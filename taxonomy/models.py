from django.db import models
from references.models import Reference
from django.core.validators import ValidationError
from django.core.exceptions import ObjectDoesNotExist

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
        #returns dictionary of all parents
        parents = {}
        if self.parent is None:
            parents[self.rank.name] = self.name
            return parents
        else:
            parents[self.rank.name] = self.name
            current = self.parent
            while current is not None:
                parents[current.rank.name] = current.name
                current = current.parent
            return parents

    def taxClass(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            taxClass = fullTaxDict["class"]
        except:
            taxClass = ""
        return taxClass

    def order(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            order = fullTaxDict["order"]
        except:
            order = ""
        return order

    def subfamily(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            subfamily = fullTaxDict["subfamily"]
        except:
            subfamily = ""
        return subfamily

    def family(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            family = fullTaxDict["family"]
        except:
            family = ""
        return family

    def tribe(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            tribe = fullTaxDict["tribe"]
        except:
            tribe = ""
        return tribe

    def genus(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            genus = fullTaxDict["genus"]
        except:
            genus = ""
        return genus

    def species(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            species = fullTaxDict["species"]
        except:
            species = ""
        return species

    def clean(self, *args, **kwargs):
        if self.parent:
            try:
                if not self.parent.rank.sortOrder == self.rank.sortOrder - 1:
                    raise ValidationError("You are entering a taxon of rank '{0}' so parent taxon must be of rank '{1}'".format(
                        Rank.objects.all().get(sortOrder=self.rank.sortOrder).name.upper(),
                        Rank.objects.all().get(sortOrder=self.rank.sortOrder - 1).name.upper())
                    )
            except ObjectDoesNotExist:
                raise ValidationError("Taxon must have a rank. This is a required field.")

        try:
            if self.parent is None and self.rank.name <> 'kingdom':
                raise ValidationError("A taxon with no parent must be at the rank of 'kingdom'.")
        except ObjectDoesNotExist:
                raise ValidationError("Taxon must have a rank. This is a required field.")

        super(Taxon, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Taxon, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "taxa"
        unique_together = ["rank", "name"]