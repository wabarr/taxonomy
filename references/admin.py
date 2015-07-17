from django.contrib import admin
from references.models import *



class AuthorOrderInline(admin.TabularInline):
    model = AuthorOrder
    extra = 2

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__']
    inlines = [AuthorOrderInline]

class ReferenceAdmin(admin.ModelAdmin):
    search_fields = []
    inlines = [AuthorOrderInline]

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Reference, ReferenceAdmin)