from django.db.models import Count
from django.db.models.functions import TruncDate
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from src.apps.history.models import SearchHistory
from .serializers import CategorySearchStatSerializer, ActiveUserStatSerializer, DailySearchStatSerializer, \
    MonthlyStatSerializer, SearchHistorySerializer
from src.apps.history.filter import SearchHistoryStatFilter
from ...apps.common.paginations import CustomPagination
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


@extend_schema(tags=["Statistics"])
class DailySearchStatViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DailySearchStatSerializer

    def get_queryset(self):
        queryset = SearchHistory.objects.annotate(
            date=TruncDate('created_at')
        ).values(
            'date'
        ).annotate(
            search_count=Count('id')
        ).order_by(
            'date'
        )
        return queryset


@extend_schema(tags=["Statistics"])
class MonthlyStatViewSet(viewsets.ViewSet):
    serializer_class = MonthlyStatSerializer

    def list(self, request):
        aggregated_data = [
            {'month': '2025-01-01', 'user_registrations': 150, 'category_searches': 450},
            {'month': '2025-02-01', 'user_registrations': 180, 'category_searches': 520},
            {'month': '2025-03-01', 'user_registrations': 210, 'category_searches': 610},
        ]

        serializer = MonthlyStatSerializer(instance=aggregated_data, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Statistics"])
class UserSearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SearchHistory.objects.select_related('user', 'category').order_by('-created_at')
    serializer_class = SearchHistorySerializer
    pagination_class = CustomPagination
