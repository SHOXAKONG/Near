import json

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from query_counter.decorators import queries_counter
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from src.apps.place.models import Place
from .serializers import PlaceSerializer
from .filters import PlaceFilter
from src.apps.common.paginations import CustomPagination
from ...apps.common.permissions import IsEntrepreneur, IsAdmin
from src.api.place.utils import convert_image


@method_decorator(queries_counter, name='dispatch')
@extend_schema(tags=["Place"])
class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdmin | IsEntrepreneur]

    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceFilter

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Place.objects.select_related('category', 'user').all()

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')

        if latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
                user_location = Point(lon, lat, srid=4326)

                queryset = queryset.annotate(
                    distance=Distance('location', user_location)
                ).order_by('distance')
            except (ValueError, TypeError):
                return Place.objects.none()

        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        location_str = data.get('location')
        if location_str and isinstance(location_str, str):
            try:
                location_data = json.loads(location_str)
                data['location'] = location_data
            except json.JSONDecodeError:
                return Response({"location": "Lokatsiya formati noto'g'ri (JSON emas)."},
                                status=status.HTTP_400_BAD_REQUEST)

        file_id = data.get('image')
        if file_id and isinstance(file_id, str):
            try:
                file_info_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={file_id}"
                file_info_res = requests.get(file_info_url)
                file_info_res.raise_for_status()
                file_path = file_info_res.json()['result']['file_path']

                file_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_path}"
                image_res = requests.get(file_url)
                image_res.raise_for_status()

                converted_image_bytes = convert_image(image_res.content, target_format='JPEG')
                image_name = f"{file_id}.jpg"
                image_content = ContentFile(converted_image_bytes, name=image_name)

                data['image'] = image_content
            except Exception as e:
                return Response({"image": f"Telegramdan rasm yuklashda xatolik: {e}"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
