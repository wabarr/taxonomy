from django.conf.urls import url, include
from django.contrib import admin
from taxonomy.models import Taxon, Rank
from references.models import Reference
from rest_framework import routers, serializers, viewsets, generics
from ajax_select import urls as ajax_select_urls

# Serializers define the API representation.
class TaxonSerializer(serializers.HyperlinkedModelSerializer):
    rank = serializers.PrimaryKeyRelatedField(queryset=Rank.objects.all())
    ref = serializers.PrimaryKeyRelatedField(queryset=Reference.objects.all(), required=False)
    parent = serializers.PrimaryKeyRelatedField(queryset=Taxon.objects.all(), required=False)

    class Meta:
        model = Taxon
        fields = ('url', 'name', 'rank', 'ref', 'parent')

# ViewSets define the view behavior.
class TaxonList(viewsets.ModelViewSet):
    serializer_class = TaxonSerializer

    def get_queryset(self):
        queryset = Taxon.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'taxa', TaxonList, base_name="taxon")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]