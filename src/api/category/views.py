from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import CategorySerializer, SubcategorySerializer
from src.apps.category.models import Category, Subcategory
from ...apps.common.permissions import RoleBasedPermission


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = [IsAuthenticated, RoleBasedPermission]


@extend_schema(tags=["SubCategory"])
class SubcategoryVieSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category']
    permission_classes = [IsAuthenticated, RoleBasedPermission]
