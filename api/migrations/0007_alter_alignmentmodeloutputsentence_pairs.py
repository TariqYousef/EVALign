# Generated by Django 4.0.6 on 2022-07-23 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_alignmentmodeloutputsentence_pairs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alignmentmodeloutputsentence',
            name='pairs',
            field=models.JSONField(default=dict, verbose_name='Translation pairs.'),
        ),
    ]
