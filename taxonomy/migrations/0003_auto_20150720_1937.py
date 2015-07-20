# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0002_auto_20150717_1515'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taxon',
            unique_together=set([('rank', 'name')]),
        ),
    ]
