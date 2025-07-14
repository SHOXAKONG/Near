from typing import Optional
from drf_spectacular.utils import extend_schema_field
from src.apps.place.models import Place
from rest_framework import serializers
from .fields import PointFieldSerializer
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

PointFieldSchema = {
    'type': 'object',
    'properties': {
        'latitude': {'type': 'number', 'format': 'double'},
        'longitude': {'type': 'number', 'format': 'double'}
    }
}


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    distance = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'name_uz', 'name_ru', 'category', 'contact', 'location', 'distance',
                  'created_at', 'updated_at', 'image_url', 'image', 'description', 'description_uz', 'description_ru']

    def get_distance(self, obj) -> Optional[float]:
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 2)
        return None

    def get_image_url(self, obj) -> str:
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

    @extend_schema_field(PointFieldSchema)
    def get_location(self, obj):
        if obj.location:
            return {
                'latitude': obj.location.y,
                'longitude': obj.location.x
            }
        return None

    def validate_image(self, image):
        img = Image.open(image)

        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        img = img.crop((left, top, right, bottom))

        img = img.resize((300, 300), Image.ANTIALIAS)

        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        new_image_file = ContentFile(buffer.getvalue(), name=image.name)

        return new_image_file
