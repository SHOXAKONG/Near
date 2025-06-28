from django.contrib.gis.db.models.functions import Distance
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.apps.common.permissions import IsAuthenticatedAndHasRole, IsAdmin, IsUser, IsEntrepreneur
from src.apps.place.utils import nearby_filter
from src.apps.common.paginations import CustomPagination
from src.api.place.serializers import PlaceSerializer
from src.apps.place.models import Place
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import Point


@extend_schema(tags=["Place"])
class PlaceViewSets(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsEntrepreneur | IsUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'subcategory']
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby(self, request, *args, **kwargs):
        if 'latitude' not in request.query_params or 'longitude' not in request.query_params:
            return Response(
                {"error": _("Latitude and longitude parameters are required.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
        except (TypeError, ValueError):
            return Response(
                {"error": _("Invalid latitude or longitude.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_location = Point(longitude, latitude, srid=4326)
        queryset = Place.objects.annotate(
            distance=Distance('location', user_location)
        ).order_by('distance')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
