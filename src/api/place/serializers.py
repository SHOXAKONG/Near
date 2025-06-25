from src.apps.place.models import Place
from rest_framework import serializers

class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'category', 'subcategory', 'latitude', 'longitude', 'contact', 'created_at', 'updated_at']

