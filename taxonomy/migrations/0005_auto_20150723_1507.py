# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0004_auto_20150721_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxon',
            name='lastModified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='parent',
            field=models.ForeignKey(verbose_name=b'parent', blank=True, to='taxonomy.Taxon', null=True),
        ),
    ]
