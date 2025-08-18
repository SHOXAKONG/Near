import logging
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from query_counter.decorators import queries_counter
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.history.models import SearchHistory
from .serializers import SearchHistorySerializer

# Setup logger
logger = logging.getLogger(__name__)


@extend_schema(tags=["SearchHistory"])
@method_decorator(queries_counter, name='dispatch')
class SearchHistoryViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = SearchHistory.objects.select_related('user', 'category')
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]  # uncomment to enforce auth

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        logger.info(f"[SearchHistory] User {self.request.user} added search history {instance.id} "
                    f"with category={instance.category} and query='{getattr(instance, 'query', None)}'")

    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)  # show only user's history
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            logger.info(f"[SearchHistory] User {request.user} listed their paginated search history "
                        f"(page size={len(page)})")
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"[SearchHistory] User {request.user} listed all their search history "
                    f"(count={queryset.count()})")
        return Response(serializer.data, status=status.HTTP_200_OK)
