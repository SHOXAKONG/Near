from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import CategorySerializer, SubcategorySerializer
from src.apps.category.models import Category, Subcategory

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = [IsAuthenticated]

class SubcategoryVieSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category']
    permission_classes = [IsAuthenticated]