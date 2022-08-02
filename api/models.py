from django.db import models
import traceback


class GsDataset(models.Model):
    title = models.CharField(verbose_name='Data set name',
                             help_text="Unique Name to be used in the frontend. eg.: De-En, En-Fr, ..etc",
                             max_length=100,
                             default="")
    src_language = models.CharField(verbose_name='Source Language Code',
                                    help_text=" ISO 639‑1 Two-letter code, for example: en, es, fr,..etc",
                                    max_length=2,
                                    default="")
    tgt_language = models.CharField(verbose_name='Target Language Code',
                                    help_text=" ISO 639‑1 Two-letter code, for example: en, es, fr,..etc",
                                    max_length=2,
                                    default="")
    meta = models.JSONField(verbose_name='Meta Information')
    stats = models.JSONField(verbose_name='Statistics')

    def get_obj_as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "src_language": self.src_language,
            "tgt_language": self.tgt_language,
            "meta": self.meta,
            "stats": self.stats,
        }

    class Meta:
        verbose_name = "Gold Standard Dataset"
        verbose_name_plural = "Gold Standard Datasets"


class GsSentence(models.Model):
    dataset = models.ForeignKey(GsDataset, on_delete=models.CASCADE)
    sentence_id = models.CharField(verbose_name='Sentence ID', max_length=10,
                                   help_text="A unique ID within the data set.")

    src_tokens = models.CharField(verbose_name='Source Language Code',
                                  help_text=" ISO 639‑1 Two-letter code, for example: en, es, fr,..etc",
                                  max_length=600,
                                  default="")

    src_length = models.IntegerField(verbose_name="Length of the source sentence",
                                     default=0)

    src_length_wo_punct = models.IntegerField(verbose_name="Length of the source sentence without punctuations",
                                              default=0)

    tgt_tokens = models.CharField(verbose_name='Target Language Code',
                                  help_text=" ISO 639‑1 Two-letter code, for example: en, es, fr,..etc",
                                  max_length=600,
                                  default="")

    tgt_length = models.IntegerField(verbose_name="Length of the target sentence",
                                     default=0)

    tgt_length_wo_punct = models.IntegerField(verbose_name="Length of the target sentence without punctuations",
                                              default=0)

    sure_alignments = models.JSONField(verbose_name='Sure Alignments')

    possible_alignments = models.JSONField(verbose_name='Possible Alignments')

    class Meta:
        unique_together = (('sentence_id', 'dataset_id'),)
        verbose_name = "Gold Standard Dataset"
        verbose_name_plural = "Gold Standard Datasets"


class AlignmentModel(models.Model):
    title = models.CharField(verbose_name='Alignment Model', unique=True,
                             help_text="Unique Name to be used in the frontend. eg.: SimAlign-, En-Fr, ..etc",
                             max_length=100,
                             default=""
                             )
    meta = models.JSONField(verbose_name='Meta Information')


class AlignmentModelOutput(models.Model):
    model = models.ForeignKey(AlignmentModel, on_delete=models.CASCADE)
    dataset = models.ForeignKey(GsDataset, on_delete=models.CASCADE)
    stats = models.JSONField(verbose_name='Statistics, Evaluation Metrics: Precision, Recall, F1, and AER')

    class Meta:
        unique_together = (('model', 'dataset'),)


class AlignmentModelOutputSentence(models.Model):
    modelOutput = models.ForeignKey(AlignmentModelOutput, on_delete=models.CASCADE)
    stats = models.JSONField(verbose_name='Statistics, Evaluation Metrics: Precision, '
                                          'Recall, F1, and AER at sentence level')
    sentence_id = models.CharField(verbose_name='Sentence ID', max_length=10)
    alignments = models.JSONField(verbose_name='Model prediction.')
    pairs = models.JSONField(verbose_name='Translation pairs.', default=dict)

    class Meta:
        unique_together = (('modelOutput_id', 'sentence_id'),)
