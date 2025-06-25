from rest_framework import serializers
from src.apps.category.models import Subcategory

class SubcategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']
