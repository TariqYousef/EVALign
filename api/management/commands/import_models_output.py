# -*- coding: utf-8 -*-
import traceback
from string import punctuation
import json
from argparse import FileType
from collections import defaultdict

from django.core.management.base import BaseCommand
from api.models import GsDataset, GsSentence, AlignmentModelOutput, AlignmentModel, AlignmentModelOutputSentence


# python manage.py import_models_output -c data/models_config/DE-EN-model_outputs.json
def convert_to_zero_indexed(tps):
    zi_tps = []
    for el in tps:
        temp = el.split("-")
        zi_tps.append(f"{int(temp[0]) - 1}-{int(temp[1]) - 1}")
    return zi_tps


def get_translation_pairs2(src, tgt, al, sure, possible):
    translation_pairs = defaultdict(lambda: 0)
    src = src.split()
    tgt = tgt.split()
    filtered = []
    src2tgt = defaultdict(lambda: [])
    tgt2src = defaultdict(lambda: [])
    for a in al:
        cls = "w"  # wrong
        temp = a.split("-")
        if a in sure:
            cls = "s"  # sure
        if a in possible:
            cls = "p"  # possible
        # try:
        s = src[int(temp[0])]
        t = tgt[int(temp[1])]
        # except IndexError as e:
        #     print(e, len(src), len(tgt), temp, "\n", al, " ".join(src), " ".join(tgt))
        filtered.append({"src": s, "tgt": t, "cls": cls, "src_id": int(temp[0]), "tgt_id": int(temp[1])})
    return filtered


def get_translation_pairs(src, tgt, al, sure, possible):
    translation_pairs = defaultdict(lambda: 0)
    src = src.split()
    tgt = tgt.split()
    filtered = []
    src2tgt = defaultdict(lambda: [])
    tgt2src = defaultdict(lambda: [])
    for a in al:
        cls = "w"  # wrong
        temp = a.split("-")
        if a in sure:
            cls = "s"  # sure
        if a in possible:
            cls = "p"  # possible
        # try:
        s = src[int(temp[0])]
        t = tgt[int(temp[1])]
        # except IndexError as e:
        #     print(e, len(src), len(tgt), temp, "\n", al, " ".join(src), " ".join(tgt))
        filtered.append({"src": s, "tgt": t, "cls": cls, "src_id": int(temp[0]), "tgt_id": int(temp[1])})
    for a in (set(sure)-set(al)):
        temp = a.split("-")
        s = src[int(temp[0])]
        t = tgt[int(temp[1])]
        filtered.append({"src": s, "tgt": t, "cls": "m", "src_id": int(temp[0]), "tgt_id": int(temp[1])})

    for a in (set(possible)-set(al)):
        temp = a.split("-")
        s = src[int(temp[0])]
        t = tgt[int(temp[1])]
        filtered.append({"src": s, "tgt": t, "cls": "m", "src_id": int(temp[0]), "tgt_id": int(temp[1])})

    return filtered


def calculate_scores_per_sentence(alignment, gold_standard, zero_indexed):
    S, P = gold_standard.sure_alignments, gold_standard.possible_alignments
    A = alignment.split()
    P = set(P).union(set(S))

    if not zero_indexed:
        A = convert_to_zero_indexed(A)

    A_P_intersection = len(set(A) & set(P))
    A_S_intersection = len(set(A) & set(S))
    AER, precision, recall, f1 = 1, 0, 0, 0
    if len(A) + len(S) > 0:
        AER = round(1 - (A_P_intersection + A_S_intersection) / (len(A) + len(S)), 2)
    if len(A) > 0:
        precision = round(A_P_intersection / len(A), 2)
    if len(S) > 0:
        recall = round(A_S_intersection / len(S), 2)
    if (precision + recall) > 0:
        f1 = round(2 * precision * recall / (precision + recall), 2)

    return {"AER": AER, "precision": precision, "recall": recall, "f1": f1, "tp": len(A),
            "A_P_intersections": A_P_intersection, "A_S_intersections": A_S_intersection}, \
           len(A), len(S), A_P_intersection, A_S_intersection


class Command(BaseCommand):
    help = 'Import Gold-Standard Dataset'

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--config",
            type=FileType("r"),
            help="Config file of the dataset",
        )

    def handle(self, *args, **options):
        # read config file
        configs = json.load(options['config'])

        for record in configs:
            try:
                dataset = GsDataset.objects.get(title=record["dataset"])
                try:
                    model = AlignmentModel.objects.get(title=record["model"])
                    amo = AlignmentModelOutput.objects.create(dataset=dataset,
                                                              model=model,
                                                              stats={})
                    idx = amo.pk

                    amo.stats = self.import_sentences(record['path_to_sentences'], idx,
                                                      dataset.pk, record.get("zero_indexed", True))
                    amo.save()
                    self._success(f"Model {record['model']} output of the {dataset.title} dataset is imported")
                except Exception as e:
                    self._error(e)# (f"Model {record['model']} doesn't match any model in the database: {e}")

            except Exception as e:
                self._error(f"Dataset {record['dataset']} doesn't match any dataset in the database: {e}")

    def import_sentences(self, path, model_id, dataset_id, zero_indexed):
        dataset = GsDataset.objects.get(pk=dataset_id)
        counter = 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                predictions = json.load(f)
        except Exception as e:
            self._error(f"Articles File couldn't be opened.\n{e}")
            exit(1)
        _sentences = GsSentence.objects.filter(dataset_id=dataset_id)
        gs_sentences = {str(sen.sentence_id): sen for sen in _sentences}
        all_A_P_intersections, all_A_S_intersections = 0, 0
        all_A, all_S = 0, 0

        for sen_id, a in predictions.items():
            g = gs_sentences[str(sen_id)]
            res = calculate_scores_per_sentence(a, g, zero_indexed)
            try:
                AlignmentModelOutputSentence.objects.create(modelOutput_id=model_id,
                                                            sentence_id=sen_id,
                                                            stats=res[0],
                                                            alignments=a.split(),
                                                            pairs=get_translation_pairs(g.src_tokens, g.tgt_tokens,
                                                                                        a.split(), g.sure_alignments,
                                                                                        g.possible_alignments))
                counter += 1
                all_A += res[1]
                all_S += res[2]
                all_A_P_intersections += res[3]
                all_A_S_intersections += res[4]
            except Exception as e:
                self._error(
                    f"Something went wrong, sentence {sen_id} of the model {model_id} couldn't be imported.\n{e}")
                print(traceback.format_exc())
        all_precision = round(all_A_P_intersections / all_A, 4)
        all_recall = round(all_A_S_intersections / all_S, 4)
        all_f1, all_AER = 0, 1
        if all_precision + all_recall > 0:
            all_f1 = round(2 * all_precision * all_recall / (all_precision + all_recall), 4)

        if all_A + all_S > 0:
            all_AER = round(1 - (all_A_P_intersections + all_A_S_intersections) / (all_A + all_S), 4)
        self._success(f"{counter} sentences are imported to the database")
        return {"AER": all_AER,
                "precision": all_precision,
                "recall": all_recall,
                "f1": all_f1,
                "tp": all_A,
                "A_P_intersections": all_A_P_intersections,
                "A_S_intersections": all_A_S_intersections,
                "missing_pairs": (dataset.stats["sure"] + dataset.stats["possible"]) - all_A_P_intersections
                }

    def _success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def log(self, msg):
        self.stdout.write(msg)

    def _error(self, msg):
        self.stderr.write(self.style.ERROR(msg))
