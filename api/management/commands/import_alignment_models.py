# -*- coding: utf-8 -*-

import json
import os
import string
from argparse import FileType

from django.core.management.base import BaseCommand

from api.models import GsDataset, GsSentence, AlignmentModel


class Command(BaseCommand):
    help = 'Import Alignment Models'

    def add_arguments(self, parser):
        parser.add_argument(
            "-i",
            "--input",
            type=FileType("r"),
            help="File contains a list of Model names and their information.",
        )

    def handle(self, *args, **options):
        # read config file
        models = json.load(options['input'])
        counter = 0
        for _model in models:
            try:
                AlignmentModel.objects.create(title=_model.get("title", ""),
                                              meta=_model.get("meta", ""))
                counter += 1
            except Exception as e:
                self._error(f"Model {_model.get('title', '')} couldn't be imported.\n{e}")
        self._success(f"{counter} models are imported to the database")

    def _success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def log(self, msg):
        self.stdout.write(msg)

    def _error(self, msg):
        self.stderr.write(self.style.ERROR(msg))
