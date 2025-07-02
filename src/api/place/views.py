from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django_filters.rest_framework import DjangoFilterBackend

from src.apps.place.models import Place
from .serializers import PlaceSerializer
from .filters import PlaceFilter
from src.apps.common.paginations import CustomPagination
from src.apps.common.permissions import IsAdmin, IsEntrepreneur, IsUser


@extend_schema(tags=["Place"])
class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated | IsUser | IsAdmin | IsEntrepreneur]

    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceFilter

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Place.objects.all()

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