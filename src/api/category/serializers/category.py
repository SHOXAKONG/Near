from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from src.apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
