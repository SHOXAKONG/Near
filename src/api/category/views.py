from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CategorySerializer
from src.apps.category.models import Category
from src.apps.common.permissions import IsAdmin, IsUser, IsEntrepreneur


class RoleBasedPermissionsMixin:
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdmin | IsEntrepreneur]


@extend_schema(tags=["Category"])
class CategoryViewSet(RoleBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

