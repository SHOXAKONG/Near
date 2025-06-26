from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import CategorySerializer, SubcategorySerializer
from src.apps.category.models import Category, Subcategory
from src.apps.common.permissions import IsAdmin, IsUser, IsEntrepreneur


class RoleBasedPermissionsMixin:
    permission_classes = [IsAuthenticated, IsAdmin | IsEntrepreneur | IsUser]

@extend_schema(tags=["Category"])
class CategoryViewSet(RoleBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


@extend_schema(tags=["SubCategory"])
class SubcategoryVieSet(RoleBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category']
