from rest_framework import serializers
from django.contrib.gis.geos import Point

class PointFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if value is None:
            return None
        return {
            "latitude": value.y,
            "longitude": value.x
        }

    def to_internal_value(self, data):
        if not data or 'latitude' not in data or 'longitude' not in data:
            raise serializers.ValidationError("Latitude va longitude majburiy.")
        try:
            return Point(float(data['longitude']), float(data['latitude']), srid=4326)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Latitude va longitude son bo'lishi kerak.")