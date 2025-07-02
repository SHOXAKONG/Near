import django_filters
from src.apps.place.models import Place

class PlaceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Place
        fields = ['name', 'category', 'subcategory']