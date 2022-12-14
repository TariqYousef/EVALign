# Generated by Django 4.0.6 on 2022-07-20 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_gssentence_src_tokens_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlignmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.JSONField(help_text='Unique Name to be used in the frontend. eg.: SimAlign-, En-Fr, ..etc', verbose_name='Alignment Model')),
                ('meta', models.JSONField(verbose_name='Meta Information')),
            ],
        ),
        migrations.CreateModel(
            name='AlignmentModelOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stats', models.JSONField(verbose_name='Statistics, Evaluation Metrics: Precision, Recall, F1, and AER')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gsdataset')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.alignmentmodel')),
            ],
        ),
        migrations.AlterField(
            model_name='gssentence',
            name='possible_alignments',
            field=models.JSONField(verbose_name='Possible Alignments'),
        ),
        migrations.AlterField(
            model_name='gssentence',
            name='sure_alignments',
            field=models.JSONField(verbose_name='Sure Alignments'),
        ),
        migrations.CreateModel(
            name='AlignmentModelOutputSentences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stats', models.JSONField(verbose_name='Statistics, Evaluation Metrics: Precision, Recall, F1, and AER at sentence level')),
                ('alignments', models.JSONField(verbose_name='Sure Alignments')),
                ('modelOutput', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.alignmentmodeloutput')),
            ],
        ),
    ]
