from django.conf.urls import url
from taxonomy.views import AddTaxa

urlpatterns = [
    url(r'^$', AddTaxa.as_view()),
]