from rest_framework import serializers
from src.apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name',]
