from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from query_counter.decorators import queries_counter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.apps.history.models import SearchHistory
from .serializers import SearchHistorySerializer

@extend_schema(tags=["SearchHistory"])
@method_decorator(queries_counter, name='dispatch')
class SearchHistoryViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        queryset = SearchHistory.objects.select_related('user', 'category')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


