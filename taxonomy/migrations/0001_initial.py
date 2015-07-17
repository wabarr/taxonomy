# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sortOrder', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('parent', models.ForeignKey(blank=True, to='taxonomy.Rank', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('parent', models.ForeignKey(blank=True, to='taxonomy.Taxon', null=True)),
                ('rank', models.ForeignKey(to='taxonomy.Rank')),
            ],
        ),
    ]
