import logging
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CategorySerializer
from src.apps.category.models import Category
from src.apps.common.permissions import IsAdmin, IsUser, IsEntrepreneur

logger = logging.getLogger(__name__)


class RoleBasedPermissionsMixin:
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdmin | IsEntrepreneur]


@extend_schema(tags=["Category"])
class CategoryViewSet(RoleBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def list(self, request, *args, **kwargs):
        logger.info(f"[CategoryViewSet] User {request.user} listed categories")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"[CategoryViewSet] User {request.user} retrieved category {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"[CategoryViewSet] User {request.user} is creating a new category with data: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"[CategoryViewSet] User {request.user} is updating category {kwargs.get('pk')} with data: {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"[CategoryViewSet] User {request.user} deleted category {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)
