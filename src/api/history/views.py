from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from src.apps.history.models import SearchHistory
from .serializers import SearchHistorySerializer


class SearchHistoryViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
