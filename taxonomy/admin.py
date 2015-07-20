from django.contrib import admin
from taxonomy.models import *
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

class RankAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sortOrder", "parent"]
    list_editable = ["name", "sortOrder", "parent"]

class TaxonAdmin(AjaxSelectAdmin):
    list_display = ["name", "rank", "parent", "ref"]
    list_filter = ["rank"]
    form = make_ajax_form(Taxon, {"parent":"taxonLookup"})


admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Rank, RankAdmin)