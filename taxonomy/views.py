from django.views.generic.edit import CreateView
from taxonomy.forms import TaxonForm
from taxonomy.models import Taxon
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

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

    @method_decorator(permission_required("Taxon.can_add", "/admin/login/"))
    def dispatch(self, *args, **kwargs):
        return super(AddTaxa, self).dispatch(*args, **kwargs)