# Generated by Django 4.0.6 on 2022-07-18 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GsDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.JSONField(help_text='Unique Name to be used in the frontend. eg.: De-En, En-Fr, ..etc', verbose_name='Data set name')),
                ('src_language', models.CharField(default='', help_text=' ISO 639‑1 Two-letter code, for example: en, es, fr,..etc', max_length=2, verbose_name='Source Language Code')),
                ('tgt_language', models.CharField(default='', help_text=' ISO 639‑1 Two-letter code, for example: en, es, fr,..etc', max_length=2, verbose_name='Target Language Code')),
                ('meta', models.JSONField(verbose_name='Meta Information')),
                ('stats', models.JSONField(verbose_name='Statistics')),
            ],
            options={
                'verbose_name': 'Gold Standard Dataset',
                'verbose_name_plural': 'Gold Standard Datasets',
            },
        ),
        migrations.CreateModel(
            name='GsSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence_id', models.JSONField(help_text='A unique ID within the data set.', verbose_name='Sentence ID')),
                ('src_tokens', models.CharField(default='', help_text=' ISO 639‑1 Two-letter code, for example: en, es, fr,..etc', max_length=2, verbose_name='Source Language Code')),
                ('src_length', models.IntegerField(default=0, verbose_name='Length of the source sentence')),
                ('src_length_wo_punct', models.IntegerField(default=0, verbose_name='Length of the source sentence without punctuations')),
                ('tgt_tokens', models.CharField(default='', help_text=' ISO 639‑1 Two-letter code, for example: en, es, fr,..etc', max_length=2, verbose_name='Target Language Code')),
                ('tgt_length', models.IntegerField(default=0, verbose_name='Length of the target sentence')),
                ('tgt_length_wo_punct', models.IntegerField(default=0, verbose_name='Length of the target sentence without punctuations')),
                ('sure_alignments', models.JSONField(verbose_name='Meta Information')),
                ('possible_alignments', models.JSONField(verbose_name='Statistics')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gsdataset')),
            ],
            options={
                'verbose_name': 'Gold Standard Dataset',
                'verbose_name_plural': 'Gold Standard Datasets',
                'unique_together': {('sentence_id', 'dataset_id')},
            },
        ),
    ]
