from django.contrib import admin
from references.models import *
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline


class AuthorOrderInline(AjaxSelectAdminTabularInline):
    model = AuthorOrder
    extra = 2
    form = make_ajax_form(AuthorOrder, {"author":"authorLookup"})


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__']
    inlines = [AuthorOrderInline]

class ReferenceAdmin(AjaxSelectAdmin):
    search_fields = []
    inlines = [AuthorOrderInline]

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Reference, ReferenceAdmin)