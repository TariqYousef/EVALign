# Generated by Django 4.0.6 on 2022-07-18 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gssentence',
            name='src_tokens',
            field=models.CharField(default='', help_text=' ISO 639‑1 Two-letter code, for example: en, es, fr,..etc', max_length=600, verbose_name='Source Language Code'),
        ),
        migrations.AlterField(
            model_name='gssentence',
            name='tgt_tokens',
            field=models.CharField(default='', help_text=' ISO 639‑1 Two-letter code, for example: en, es, fr,..etc', max_length=600, verbose_name='Target Language Code'),
        ),
    ]
