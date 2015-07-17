from django.contrib import admin
from taxonomy.models import *

class RankAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sortOrder", "parent"]
    list_editable = ["name", "sortOrder", "parent"]

class TaxonAdmin(admin.ModelAdmin):
    list_display = ["name", "rank", "parent", "ref"]
    list_filter = ["rank"]



admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Rank, RankAdmin)