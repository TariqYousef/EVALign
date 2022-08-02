# -*- coding: utf-8 -*-

import json
import os
import string
from argparse import FileType

from django.core.management.base import BaseCommand

from api.models import GsDataset, GsSentence


# python manage.py import_gs_dataset -c ~/Desktop/AlignmentEvaluation/data/ds_config/DE-EN.json

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
        all_ds_configs = json.load(options['config'])

        for configs in all_ds_configs:
            # 1 - Create a new dataset record
            ds = GsDataset(title=configs.get("title", ""),
                           src_language=configs.get("src_language", ""),
                           tgt_language=configs.get("tgt_language", ""),
                           meta=configs.get("meta", ""),
                           stats={})
            try:
                ds.save()
                self._success(f"Dataset record is created, dataset id is {ds.pk}")
            except Exception as e:
                self._error(f"Dataset record couldn't be created: {e}")
                exit(1)

            dataset_id = ds.pk

            # 2 - import dataset sentences, in the meanwhile calculate stats
            ds.stats = self.import_gs_sentence(configs['path_to_sentences'],
                                               dataset_id,
                                               configs.get("zero_indexed", False))
            ds.save()

    def import_gs_sentence(self, path, dataset_id, zero_indexed):
        try:
            with open(path, "r", encoding="utf-8") as f:
                sentences = json.load(f)
        except Exception as e:
            self._error(f"Articles File couldn't be opened.\n{e}")
            exit(1)

        created_sentences = 0
        src_length, tgt_length, src_length_wo, tgt_length_wo, sure_count, poss_count = 0, 0, 0, 0, 0, 0
        for sen in sentences:
            _src_length, _tgt_length = 0, 0
            try:
                sure_count += len(sen["sure"])
                poss_count += len(sen["possible"])
                for token in sen.get("src", "").split():
                    _src_length += 1
                    if token not in string.punctuation:
                        src_length_wo += 1

                for token in sen.get("tgt", "").split():
                    _tgt_length += 1
                    if token not in string.punctuation:
                        tgt_length_wo += 1

                sure, poss = sen["sure"], sen["possible"]
                src_length += _src_length
                tgt_length += _tgt_length

                if not zero_indexed:
                    sure, poss = self.convert_to_zero_indexed(sen["sure"]), self.convert_to_zero_indexed(
                        sen["possible"])
                defaults = {"src_tokens": sen.get("src", ""), "src_length": _src_length,
                            "tgt_tokens": sen.get("tgt", ""), "tgt_length": _tgt_length,
                            "sure_alignments": sure, "possible_alignments": poss}

                obj, created = GsSentence.objects.get_or_create(sentence_id=sen.get("id", ""),
                                                                dataset_id=dataset_id, defaults=defaults)
                if created:
                    created_sentences += 1
            except Exception as e:
                self._error(f"Sentence couldn't be inserted.\n{e}\n{sen}")
                exit(1)

        self._success(f"{created_sentences} sentences are copied to the database")
        return {
            "sentences": len(sentences),
            "src_tokens": src_length,
            "src_tokens_wo_punct": src_length_wo,
            "tgt_tokens": tgt_length,
            "tgt_tokens_wo_punct": tgt_length_wo,
            "sure": sure_count,
            "possible": poss_count
        }

    def convert_to_zero_indexed(self, tps):
        zi_tps = []
        for el in tps:
            temp = el.split("-")
            zi_tps.append(f"{int(temp[0]) - 1}-{int(temp[1]) - 1}")
        return zi_tps

    def _success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def log(self, msg):
        self.stdout.write(msg)

    def _error(self, msg):
        self.stderr.write(self.style.ERROR(msg))
