from src.apps.place.models import Place
from rest_framework import serializers
from .fields import PointFieldSerializer


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    distance = serializers.SerializerMethodField()
    location = PointFieldSerializer()
    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'name_uz', 'name_ru', 'category', 'contact', 'location', 'distance', 'created_at',
                  'updated_at', 'image_url', 'image', 'description', 'description_uz', 'description_ru']

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 2)
        return None

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None
