from django.conf.urls import url, include
from taxonomy.models import Taxon, Rank
from references.models import Reference, Author, AuthorOrder
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views


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


class FullTaxonHierarchySerializer(serializers.HyperlinkedModelSerializer):
    fullTaxonomy = serializers.CharField()

    class Meta:
        model = Taxon
        fields = ('id','fullTaxonomy')

class FullTaxonHierarchyList(viewsets.ModelViewSet):
    serializer_class = FullTaxonHierarchySerializer

    def get_queryset(self):
        queryset = Taxon.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    label = serializers.CharField(source='__unicode__')
    value = serializers.IntegerField(source='id')
    class Meta:
        model = Reference
        fields = ('label', 'value')

class ReferenceList(viewsets.ModelViewSet):
    serializer_class = ReferenceSerializer
    # set up to work with jQuery autocomplete, which sends a query string called "term"
    def get_queryset(self):
        queryset = Reference.objects.all()
        term = self.request.query_params.get('term', None)
        if term is not None:
            queryset = queryset.filter(authors__lastName__icontains=term)
        return queryset

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', '__unicode__')

class AuthorList(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

class AuthorOrderSerializer(serializers.HyperlinkedModelSerializer):
    authorString = serializers.CharField(source='author')
    referenceString = serializers.CharField(source='reference')
    class Meta:
        model = AuthorOrder
        fields = ('id', 'authorString', 'referenceString', 'orderNumber')

class AuthorOrderList(viewsets.ModelViewSet):
    serializer_class = AuthorOrderSerializer
    queryset = AuthorOrder.objects.all()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'taxa', TaxonList, base_name="taxon")
router.register(r'references', ReferenceList, base_name="reference")
router.register(r'authors', AuthorList, base_name="author")
router.register(r'author_orders', AuthorOrderList, base_name="author_order")
router.register(r'full_taxon_hierarchy', FullTaxonHierarchyList, base_name="full_taxon_hierarchy")

urlpatterns = [
    url(r'^', include(router.urls)),
    ## the next two are the login and logout view for the browsable API
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]