from django.views.generic.edit import CreateView
from taxonomy.forms import TaxonForm

class AddTaxa(CreateView):
    form_class = TaxonForm
    template_name = 'addTaxa.html'
    success_url = '/home/'
