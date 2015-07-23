from django import forms
from taxonomy.models import Taxon, Reference
from ajax_select import make_ajax_field

class TaxonForm(forms.ModelForm):
    class Meta:
        model = Taxon
        exclude = []
    parent  = make_ajax_field(Taxon, 'parent', 'taxonLookup')
    ref = make_ajax_field(Taxon, 'ref', 'referenceLookup')
    rank = make_ajax_field(Taxon, 'rank', 'rankLookup')