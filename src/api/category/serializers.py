from src.apps.category.models import Category, Subcategory
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name']


class SubcategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer(source='category')

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']
