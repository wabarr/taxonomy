from django.contrib import admin
from taxonomy.models import *
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views import main
from django.http import HttpResponseRedirect

class OrderFilter(SimpleListFilter):
    title = 'order'
    parameter_name = 'rank'

    def lookups(self, request, model_admin):
        orders = set([t.order() for t in model_admin.model.objects.all()])
        return [(t.id, t.name) for t in orders if t is not None]

    def queryset(self, request, queryset):
        if self.value():
            return Taxon.objects.childrenOf(self.value)
        else:
            return queryset

class FamilyFilter(SimpleListFilter):
    title = 'family'
    parameter_name = 'family'

    def lookups(self, request, model_admin):
        families = set([t.family() for t in model_admin.model.objects.all()])
        return [(t.id, t.name) for t in families if t is not None]

    def queryset(self, request, queryset):
        if self.value():
            return Taxon.objects.childrenOf(self.value)
        else:
            return queryset


class RankAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sortOrder", "parent"]
    list_editable = ["name", "sortOrder", "parent"]



def bulk_update(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect("/bulk_update/?ids=%s" % (",".join(selected)))

bulk_update.short_description = "Bulk update selected records"

class TaxonAdmin(AjaxSelectAdmin):
    search_fields = ('name',)
    list_editable = ["extant",]
    list_display =  ["order", "family", "subfamily", "tribe", "genus", "species", "extant"]
    list_filter = ['rank',OrderFilter,FamilyFilter]
    form = make_ajax_form(Taxon, {"parent":"taxonLookup"})
    actions = [bulk_update]

    def __init__(self,*args,**kwargs):
        super(TaxonAdmin, self).__init__(*args, **kwargs)
        main.EMPTY_CHANGELIST_VALUE = '-'







admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Rank, RankAdmin)