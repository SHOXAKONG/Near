from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .subcategory import SubcategorySerializer
from src.apps.category.models import Category, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']

    @extend_schema_field(SubcategorySerializer(many=True))
    def get_subcategories(self, obj):
        return SubcategorySerializer(obj.subcategories.all(), many=True).data