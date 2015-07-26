from django.conf.urls import url
from taxonomy.views import AddTaxa, TaxonList

urlpatterns = [
    url(r'^add/$', AddTaxa.as_view(), name="add-taxon"),
    url(r'', TaxonList.as_view(), name="taxon-list")
]