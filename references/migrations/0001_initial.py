# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstName', models.CharField(max_length=30, null=True, blank=True)),
                ('middleName', models.CharField(max_length=30, null=True, blank=True)),
                ('lastName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orderNumber', models.IntegerField()),
                ('author', models.ForeignKey(to='references.Author')),
            ],
            options={
                'ordering': ['reference', 'orderNumber'],
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('title', models.CharField(max_length=200, null=True, blank=True)),
                ('journal', models.CharField(max_length=100, null=True, blank=True)),
                ('volume', models.IntegerField(null=True, blank=True)),
                ('issue', models.IntegerField(null=True, blank=True)),
                ('pages', models.CharField(max_length=20, null=True, blank=True)),
                ('doi', models.CharField(max_length=100, null=True, blank=True)),
                ('authors', models.ManyToManyField(to='references.Author', through='references.AuthorOrder')),
            ],
        ),
        migrations.AddField(
            model_name='authororder',
            name='reference',
            field=models.ForeignKey(to='references.Reference'),
        ),
    ]
