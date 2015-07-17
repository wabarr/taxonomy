# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0001_initial'),
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rank',
            options={'ordering': ['sortOrder']},
        ),
        migrations.AlterModelOptions(
            name='taxon',
            options={'verbose_name_plural': 'taxa'},
        ),
        migrations.AddField(
            model_name='taxon',
            name='ref',
            field=models.ForeignKey(blank=True, to='references.Reference', null=True),
        ),
    ]
