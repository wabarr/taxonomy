from ajax_select import LookupChannel
from references.models import Author, Reference
from django.db.models import Q

class AuthorLookup(LookupChannel):

    model = Author

    def get_query(self, q, request):
        query = Q(firstName__icontains=q) | Q(middleName__icontains=q) | Q(lastName__icontains=q)
        return Author.objects.filter(query)

class ReferenceLookup(LookupChannel):

    model = Reference

    def get_query(self, q, request):
        query = Q(authors__firstName__icontains=q) | Q(authors__middleName__icontains=q) | Q(authors__lastName__icontains=q)
        return Reference.objects.filter(query)