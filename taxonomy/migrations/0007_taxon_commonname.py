# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0006_auto_20150727_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxon',
            name='commonName',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
