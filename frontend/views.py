from django.shortcuts import render
from api.models import *


# Create your views here.

def getDatasetsList():
    datasets = GsDataset.objects.all()
    datasets_list = [{"id": dataset.pk,
                      "title": dataset.title,
                      "meta": dataset.meta,
                      "stats": dataset.stats,
                      "src_language": dataset.src_language,
                      "tgt_language": dataset.tgt_language,
                      "models": len(AlignmentModelOutput.objects.filter(dataset_id=dataset.pk)),
                      "sure_pre": int(
                          dataset.stats["sure"] * 100 / (dataset.stats["sure"] + dataset.stats["possible"])),
                      "poss_pre": int(
                          dataset.stats["possible"] * 100 / (dataset.stats["sure"] + dataset.stats["possible"])),
                      } for dataset in datasets]
    return datasets_list


def getModelsList():
    _models = AlignmentModel.objects.all()
    _models_list = [{"id": model.pk,
                     "title": model.title,
                     "meta": model.meta,
                     "datasets": len(AlignmentModelOutput.objects.filter(model_id=model.pk)),
                     } for model in _models]
    return _models_list


language2color = {'EN': 'red-800', 'ES': 'orange-600', 'DE': 'amber-500', 'FR': 'sky-600',
                  'PT': 'pink-700', 'RO': 'rose-600', 'CZ': 'purple-600', 'HI': 'emerald-600'}

code2lang = {'EN': 'English', 'ES': 'Spanish', 'DE': 'German', 'FR': 'French',
             'PT': 'Portuguese', 'RO': 'Romanian', 'CZ': 'Czech', 'HI': 'Hindi'}


def index(request):
    context = {
        "datasets": getDatasetsList(),
        "language2color": language2color,
        "code2lang": code2lang
    }
    return render(request, 'frontend/index.html', context)


def about(request):
    context = {
    }
    return render(request, 'frontend/about.html', context)


def main(request):
    context = {
    }
    return render(request, 'frontend/main.html', context)


def model(request):
    model_id = request.GET.get('m', '')
    _models = AlignmentModelOutput.objects.filter(model_id=model_id)
    datasets = [m.dataset.get_obj_as_dict() for m in _models]
    context = {
        "datasets": datasets,
        "language2color": language2color,
        "code2lang": code2lang,
        "model_id": model_id
    }
    return render(request, 'frontend/model.html', context)


def models(request):
    context = {
        "models": getModelsList(),
    }
    return render(request, 'frontend/models.html', context)
