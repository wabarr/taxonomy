# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_auto_20150723_1507'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taxon',
            unique_together=set([('name', 'parent')]),
        ),
    ]
