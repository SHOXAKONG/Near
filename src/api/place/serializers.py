from src.apps.place.models import Place
from rest_framework import serializers
from .fields import PointFieldSerializer

class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    distance = serializers.SerializerMethodField()
    location = PointFieldSerializer()

    class Meta:
        model = Place
        fields = ['id', 'name', 'category', 'subcategory', 'contact', 'location', 'distance', 'created_at',
                  'updated_at', 'image', 'description']

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 2)
        return None