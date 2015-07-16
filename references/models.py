from django.db import models

class Author(models.Model):
    firstName = models.CharField(max_length=30, blank=True, null=True)
    middleName = models.CharField(max_length=30, blank=True, null=True)
    lastName = models.CharField(max_length=30)

    def __unicode__(self):
        return " ".join([self.firstName, self.middleName, self.lastName])

class Reference(models.Model):
    authors = models.ManyToManyField(Author, through="AuthorOrder")
    year = models.IntegerField()
    journal = models.CharField(max_length=100, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    issue = models.IntegerField(blank=True, null=True)
    pages = models.CharField(max_length=20, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        lastNames = []
        for author in self.authors.all().order_by("authororder__orderNumber"):
            lastNames.append(author.lastName)

        if len(lastNames) == 1 :
            return "(" + lastNames[0] + ", " + str(self.year) + ")"
        if len(lastNames) == 2 :
            return "(" + ' & '.join(lastNames) + ", " + str(self.year) + ")"
        if len(lastNames) > 2 :
            return "(" + lastNames[0] + " et al." + ", " + str(self.year) + ")"

class AuthorOrder(models.Model):
    reference = models.ForeignKey(Reference)
    author = models.ForeignKey(Author)
    orderNumber = models.IntegerField()
    class Meta:
        ordering = ["reference", "orderNumber"]