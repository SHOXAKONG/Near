from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from src.apps.history.models import SearchHistory
from .serializers import CategorySearchStatSerializer, ActiveUserStatSerializer
from src.apps.history.filter import SearchHistoryStatFilter
from ...apps.users.models import Users


@extend_schema(tags=["Statistics"])
class SearchHistoryStatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySearchStatSerializer
    filterset_class = SearchHistoryStatFilter

    def get_queryset(self):
        queryset = SearchHistory.objects.values(
            'category',
            'category__name'
        ).annotate(
            search_count=Count('category')
        ).order_by(
            '-search_count'
        )
        return queryset

@extend_schema(tags=["Statistics"])
class ActiveUserStatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ActiveUserStatSerializer

    def get_queryset(self):
        queryset = Users.objects.annotate(
            total_searches=Count('search_history')
        ).filter(
            total_searches__gt=0
        ).order_by(
            '-total_searches'
        )
        return queryset
