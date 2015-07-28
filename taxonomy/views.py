from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from taxonomy.forms import TaxonForm
from taxonomy.models import Taxon
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.forms.models import modelform_factory

class TaxonList(TemplateView):
    template_name = 'taxa_list.html'

class ChangeTaxon(SuccessMessageMixin, UpdateView):
    template_name = 'changeTaxon.html'
    model = Taxon
    form_class = TaxonForm
    success_message = "Successfully edited this taxon."

    @method_decorator(permission_required("Taxon.can_change", "/admin/login/"))
    def dispatch(self, *args, **kwargs):
        return super(ChangeTaxon, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("change-taxon", args=[self.object.id])

def bulk_update(request):
    ids = request.GET.get("ids", "")
    qst = Taxon.objects.filter(id__in=ids.split(','))
    # we can't use our existing TaxonForm, because it has ajaxselects fields and they screw it up
    basicTaxonForm = modelform_factory(Taxon, exclude=[])
    if request.method == 'POST':
        updatedFieldName = [key for key in request.POST.keys() if not "_text" in key if not "csrf" in key]
        updatedFieldName = updatedFieldName[0]
        for taxon in qst:
            try:
                templateForm = basicTaxonForm(instance=taxon)
                newData = templateForm.initial
                newData[updatedFieldName] = request.POST.get(updatedFieldName,None)
                theForm = basicTaxonForm(instance=taxon, data=newData)

                if theForm.is_valid():
                    theForm.save()
                else:
                    messages.error(request, "Form did not validate. Check your entry.")
                    return HttpResponseRedirect(request.get_full_path())
            except:
                messages.error(request, "There was an exception. Object hasn't been saved, but you are exceptional.")
                return HttpResponseRedirect(request.get_full_path())
        messages.success(request, "Successfully updated {0} taxa".format(len(qst)))
        return HttpResponseRedirect("/admin/taxonomy/taxon/")
    else:
        return render_to_response('bulk_update.html',
                                  {'form': TaxonForm(), "queryset": qst},
                                  context_instance=RequestContext(request))

class AddTaxa(SuccessMessageMixin, CreateView):
    form_class = TaxonForm
    template_name = 'addTaxa.html'
    success_url = '/add/'
    success_message = "Success!"

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

    def get_success_message(self, cleaned_data):
        #  cleaned_data is the cleaned data from the form which is used for string formatting
        return "{0} was succesfully added".format(self.object)