from collections import defaultdict

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from api.models import *
from django.core import serializers


def get_alignments(alignments):
    _ret = []
    for el in alignments:
        temp = el.split("-")
        _ret.append([int(temp[0]), int(temp[1])])
    return _ret


def prepare_gold_standard(sure, possible):
    gs = []
    for el in sure:
        temp = el.split("-")
        gs.append([int(temp[0]), int(temp[1]), "s"])
    for el in possible:
        temp = el.split("-")
        gs.append([int(temp[0]), int(temp[1]), "p"])
    return gs


def findPair(request):
    dataset_id = request.GET.get('ds_id', '')
    model = request.GET.get('m', '')
    src = request.GET.get('src', '')
    tgt = request.GET.get('tgt', '')
    cls = request.GET.get('cls', 'w')
    gs_sentences = GsSentence.objects.filter(dataset_id=int(dataset_id))
    _models = AlignmentModelOutput.objects.filter(dataset_id=dataset_id)
    almos = AlignmentModelOutputSentence.objects.filter(Q(modelOutput__dataset_id=dataset_id) &
                                                        Q(modelOutput__model_id=model),
                                                        pairs__contains=[{'src': src,
                                                                          'tgt': tgt,
                                                                          'cls': cls}])
    models_predictions = defaultdict(lambda: {})
    ids = []
    for sen in almos:
        ids.append(sen.sentence_id)
    almos = AlignmentModelOutputSentence.objects.filter(modelOutput__dataset_id=dataset_id, sentence_id__in=ids)
    for sen in almos:
        models_predictions[sen.modelOutput.model_id][sen.sentence_id] = \
            {"alignment": get_alignments(sen.alignments), "stat": sen.stats, "pairs": sen.pairs}
    sentences = []

    for sen in gs_sentences:
        if sen.sentence_id in ids:
            obj = {"src": sen.src_tokens.split(),
                   "tgt": sen.tgt_tokens.split(),
                   "src_length": sen.src_length,
                   "tgt_length": sen.tgt_length,
                   "gs": prepare_gold_standard(sen.sure_alignments, sen.possible_alignments),
                   "id": sen.sentence_id}

            for m in _models:
                obj[f"{m.model.title}"] = models_predictions[m.model.pk][sen.sentence_id]
            sentences.append(obj)

    return JsonResponse({"gs_sentences": sentences})


def search(request):
    # Retrieve Parameters
    dataset_id = request.GET.get('ds_id', '')
    term = request.GET.get('q', '')
    language = request.GET.get('c', '')
    model = request.GET.get('m', '')
    term_regex = r"\y{0}\y".format(term)
    # Build the query
    cond = Q()
    if term.strip() != "":
        cond = Q(src_tokens__iregex=term_regex)
        if language == "tgt":
            cond = Q(tgt_tokens__iregex=term_regex)
    # Get sentences
    gs_sentences = GsSentence.objects.filter(dataset_id=int(dataset_id)).filter(cond).order_by('sentence_id')
    # Get Models related to the dataset and their outputs
    _models = AlignmentModelOutput.objects.filter(dataset_id=dataset_id)
    almos = AlignmentModelOutputSentence.objects.filter(modelOutput__dataset_id=dataset_id)
    models_predictions = defaultdict(lambda: {})
    for sen in almos:
        models_predictions[sen.modelOutput.model_id][sen.sentence_id] = \
            {"alignment": get_alignments(sen.alignments), "stat": sen.stats, "pairs": sen.pairs}
    sentences = []

    # Prepare the values for the frontend
    for sen in gs_sentences:
        obj = {"src": sen.src_tokens.split(),
               "tgt": sen.tgt_tokens.split(),
               "src_length": sen.src_length,
               "tgt_length": sen.tgt_length,
               "gs": prepare_gold_standard(sen.sure_alignments, sen.possible_alignments),
               "id": sen.sentence_id}
        for m in _models:
            obj[f"{m.model.title}"] = models_predictions[m.model.pk][sen.sentence_id]
        sentences.append(obj)

    return JsonResponse({"gs_sentences": sentences})


def getModel(request):
    model_id = request.GET.get('m', '')
    try:
        model = AlignmentModel.objects.get(id=model_id)
        _models = AlignmentModelOutput.objects.filter(model_id=model_id)
        return JsonResponse({"model": {"title": model.title, "meta": model.meta},
                             "datasets": [{"model_id": m.model.pk,
                                           "model_output_id": m.pk,
                                           "dataset": m.dataset.get_obj_as_dict(),
                                           "title": m.model.title,
                                           "meta": m.model.meta,
                                           "stat": m.stats
                                           } for m in _models]}, safe=False)
    except ObjectDoesNotExist as e:
        return JsonResponse({"datasets": []}, safe=False)


def getModelsByDatasetID(request):
    dataset_id = request.GET.get('ds_id', '')
    try:
        dataset = GsDataset.objects.get(id=int(dataset_id))
        gs_sentences = GsSentence.objects.filter(dataset_id=int(dataset_id))
        _models = AlignmentModelOutput.objects.filter(dataset_id=dataset_id)
        models_id2title = {m.model.pk: m.model.title for m in _models}
        almos = AlignmentModelOutputSentence.objects.filter(modelOutput__dataset_id=dataset_id)
        models_predictions = defaultdict(lambda: {})
        for sen in almos:
            models_predictions[sen.modelOutput.model_id][sen.sentence_id] = \
                {"alignment": get_alignments(sen.alignments), "stat": sen.stats, "pairs": sen.pairs}
        sentences = []
        for sen in gs_sentences:
            obj = {"src": sen.src_tokens.split(),
                   "tgt": sen.tgt_tokens.split(),
                   "src_length": sen.src_length,
                   "tgt_length": sen.tgt_length,
                   "gs": prepare_gold_standard(sen.sure_alignments, sen.possible_alignments),
                   "id": sen.sentence_id}
            for m in _models:
                obj[f"{m.model.title}"] = models_predictions[m.model.pk][sen.sentence_id]
            sentences.append(obj)

        return JsonResponse({"gs_sentences": sentences,
                             "dataset": dataset.get_obj_as_dict(),
                             "models": [{"model_id": m.model.pk,
                                         "model_output_id": m.pk,
                                         "title": m.model.title,
                                         "meta": m.model.meta,
                                         "stat": m.stats
                                         } for m in _models]}, safe=False)
    except ObjectDoesNotExist as e:
        return JsonResponse({"models": []}, safe=False)


def getWrongTranslationPairs(request):
    dataset_id = request.GET.get('ds_id', '')
    model = request.GET.get('m', '')
    cls = request.GET.get('cls', 'w')

    almos = AlignmentModelOutputSentence.objects.filter(Q(modelOutput__dataset_id=dataset_id) &
                                                        Q(modelOutput__model_id=model))
    wrong_alignemts = defaultdict(lambda: 0)
    for sentence in almos:
        for pair in sentence.pairs:
            if pair["cls"] == cls:
                wrong_alignemts[f"{pair['src']}__{pair['tgt']}"] += 1
    sorted_pairs = sorted(wrong_alignemts.items(), key=lambda x: x[1], reverse=True)
    ret = []
    for pair in sorted_pairs:
        temp = pair[0].split("__")
        ret.append({"src": temp[0], "tgt": temp[1], "cls": cls, "freq": pair[1]})
    return JsonResponse({"pairs": ret})

# def getWrongAlignments(request):
