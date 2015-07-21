# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0003_auto_20150720_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxon',
            name='extant',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
