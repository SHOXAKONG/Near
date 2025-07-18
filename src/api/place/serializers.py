import json
from rest_framework import serializers
from django.contrib.gis.geos import Point
from typing import Optional

from src.apps.place.models import Place


class CustomPointField(serializers.Field):

    def to_representation(self, value):
        if value is None:
            return None
        return {'latitude': value.y, 'longitude': value.x}

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Location string is not valid JSON.")

        if not isinstance(data, dict) or 'latitude' not in data or 'longitude' not in data:
            raise serializers.ValidationError("Location must be a dictionary with 'latitude' and 'longitude' keys.")

        try:
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
        except (ValueError, TypeError):
            raise serializers.ValidationError("Latitude and longitude must be valid numbers.")

        return Point(longitude, latitude, srid=4326)


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    distance = serializers.SerializerMethodField()
    location = CustomPointField(read_only=True)
    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Place
        fields = ['id', 'name', 'name_uz', 'name_ru', 'category', 'contact', 'location', 'distance',
                  'created_at', 'updated_at', 'image_url', 'image', 'description', 'description_uz', 'description_ru']

    def get_distance(self, obj) -> Optional[float]:
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 2)
        return None

    def get_image_url(self, obj) -> Optional[str]:
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None


class PlaceCreateUpdateSerializer(serializers.ModelSerializer):
    location = CustomPointField()
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Place
        fields = ['name', 'name_uz', 'name_ru', 'category', 'contact', 'location',
                  'image', 'description', 'description_uz', 'description_ru']
