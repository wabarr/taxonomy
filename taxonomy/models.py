from django.db import models


class Rank(models.Model):
    sortOrder = models.IntegerField()
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True)

class Taxon(models.Model):
    rank = models.ForeignKey(Rank)
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True)