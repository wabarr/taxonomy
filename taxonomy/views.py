from django.views.generic.edit import CreateView
from taxonomy.forms import TaxonForm
from taxonomy.models import Taxon

class AddTaxa(CreateView):
    form_class = TaxonForm
    template_name = 'addTaxa.html'
    success_url = '/home/'

    def get_initial(self):
        lastModified = Taxon.objects.all().order_by("-lastModified")[0]
        return {
            "parent": lastModified.parent.id,
            "rank": lastModified.rank.id,
            "ref": lastModified.ref.id
        }
