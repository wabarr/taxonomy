from django.conf.urls import url
from taxonomy.views import AddTaxa, TaxonList

urlpatterns = [
    url(r'^add/', AddTaxa.as_view()),
    url(r'^$', TaxonList.as_view())
]