from django.conf.urls import url
from taxonomy.views import *

urlpatterns = [
    url(r'^add/$', AddTaxa.as_view(), name="add-taxon"),
    url(r'^update/(?P<pk>\d+)/$', ChangeTaxon.as_view(), name="change-taxon"),
    url(r'', TaxonList.as_view(), name="taxon-list")
]