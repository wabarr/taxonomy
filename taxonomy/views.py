from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from taxonomy.forms import TaxonForm
from taxonomy.models import Taxon
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

class TaxonList(TemplateView):
    template_name = 'taxa_list.html'

class ChangeTaxon(UpdateView):
    template_name = 'changeTaxon.html'
    model = Taxon
    form_class = TaxonForm

    @method_decorator(permission_required("Taxon.can_change", "/admin/login/"))
    def dispatch(self, *args, **kwargs):
        return super(ChangeTaxon, self).dispatch(*args, **kwargs)

class AddTaxa(CreateView):
    form_class = TaxonForm
    template_name = 'addTaxa.html'
    success_url = '/add/'

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

    @method_decorator(permission_required("Taxon.can_add", "/admin/login/"))
    def dispatch(self, *args, **kwargs):
        return super(AddTaxa, self).dispatch(*args, **kwargs)