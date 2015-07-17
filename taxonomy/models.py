from django.db import models
from references.models import Reference


class Rank(models.Model):
    sortOrder = models.IntegerField()
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["sortOrder"]

class Taxon(models.Model):
    rank = models.ForeignKey(Rank)
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True)
    ref = models.ForeignKey(Reference, null=True, blank=True)

    def __unicode__(self):
        return self.name + " (" + str(self.rank).upper() + ")"

    def fullTaxonomy(self):
        #returns ordered list of all parent taxa
        if self.parent is None:
            return None

        else:
            parents = []
            parents.append(self)
            current = self.parent
            while current is not None:
                parents.append(current.parent)
                current = current.parent
            return [element for element in reversed(parents) if element is not None]

    class Meta:
        verbose_name_plural = "taxa"