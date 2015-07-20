from django.db import models
from references.models import Reference
from django.core.validators import ValidationError

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
            return [self.__str__()]

        else:
            parents = []
            parents.append(self)
            current = self.parent
            while current is not None:
                parents.append(current)
                current = current.parent

            return [element.__str__() for element in reversed(parents) if element is not None]

    def clean(self, *args, **kwargs):
        if self.parent:
            if not self.parent.rank.sortOrder < self.rank.sortOrder:
                raise ValidationError("Parent taxon much be from a more inclusive taxon in the hierarchy")
        if self.parent is None and self.rank.name <> 'kingdom':
            raise ValidationError("A taxon with no parent must be at the rank of 'kingdom'.")

        super(Taxon, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Taxon, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "taxa"