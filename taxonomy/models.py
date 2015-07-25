from django.db import models
from references.models import Reference
from django.core.validators import ValidationError
from django.core.exceptions import ObjectDoesNotExist

class TaxonManager(models.Manager):
    def childrenOf(self, taxonID):
        children = []
        parent = Taxon.objects.get(pk=taxonID)
        for taxon in Taxon.objects.all():
            #if the name of the taxon in question appears in the full taxonomy of a taxon, include it in the filter
            if parent.name in taxon.fullTaxonomy().values():
                children.append(taxon.id)
        return Taxon.objects.filter(id__in=children)

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
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="parent")
    ref = models.ForeignKey(Reference, null=True, blank=True)
    extant = models.NullBooleanField(default=True)
    notes = models.TextField(null=True, blank=True)
    lastModified = models.DateTimeField(auto_now=True, null=True)
    objects = TaxonManager()
    def __unicode__(self):
        #return self.name + " (" + str(self.rank).upper() + ")"
        if self.rank.name == "species":
            return " ".join([self.parent.name, self.name])
        else:
            return self.name

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

    #TODO abstract all the different classes, the following doesn't work yet
    # def getSpecifiedParent(self, rankID):
    #     rankObject = Rank.objects.get(pk=rankID)
    #     fullTaxDict = self.fullTaxonomy()
    #     try:
    #         parent = Taxon.objects.get(rank=rankObject, name=fullTaxDict[rankObject.name])
    #     except ObjectDoesNotExist:
    #         order = None
    #     return order

    def taxClass(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            taxClass = Taxon.objects.get(rank__name="class", name=fullTaxDict["class"])
        except:
            taxClass = None
        return taxClass

    def order(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            order = Taxon.objects.get(rank__name="order", name=fullTaxDict["order"])
        except:
            order = None
        return order

    def family(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            family = Taxon.objects.get(rank__name="family", name=fullTaxDict["family"])
        except:
            family = None
        return family

    def subfamily(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            subfamily = Taxon.objects.get(rank__name="subfamily", name=fullTaxDict["subfamily"])
        except:
            subfamily = None
        return subfamily

    def tribe(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            tribe = Taxon.objects.get(rank__name="tribe", name=fullTaxDict["tribe"])
        except:
            tribe = None
        return tribe

    def genus(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            genus = Taxon.objects.get(rank__name="genus", name=fullTaxDict["genus"])
        except:
            genus = None
        return genus

    def species(self):
        fullTaxDict = self.fullTaxonomy()
        try:
            species = Taxon.objects.get(rank__name="species", name=fullTaxDict["species"])
        except:
            species = None
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