from ajax_select import LookupChannel
from references.models import Author
from django.db.models import Q

class AuthorLookup(LookupChannel):

    model = Author

    def get_query(self, q, request):
        query = Q(firstName__icontains=q) | Q(middleName__icontains=q) | Q(lastName__icontains=q)
        return Author.objects.filter(query)