from django_filters import rest_framework as filters
from .models import SearchHistory


class SearchHistoryStatFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    user = filters.NumberFilter(field_name='user__id')

    class Meta:
        model = SearchHistory
        fields = ['created_at', 'user']