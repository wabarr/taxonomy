from django.views.generic.edit import CreateView
from taxonomy.forms import TaxonForm
from taxonomy.models import Taxon

class AddTaxa(CreateView):
    form_class = TaxonForm
    template_name = 'addTaxa.html'
    success_url = '/home/'

    def get_initial(self):

        lastModified = Taxon.objects.all().order_by("-lastModified")[0]

        try:
            parent = lastModified.parent.id
        except:
            parent = None

        try:
            rank = lastModified.rank.id
        except:
            rank = None

        try:
            ref = lastModified.ref.id
        except:
            ref = None

        return {
                "parent": parent,
                "rank": rank,
                "ref": ref
            }
