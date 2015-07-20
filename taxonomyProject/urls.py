from django.conf.urls import url, include
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
from RESTful import urls as API_urls
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^API/', include(API_urls)),
    url(r'^$', RedirectView.as_view(url="/API/")),

]