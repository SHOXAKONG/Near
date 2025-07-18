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
from .serializers import PlaceSerializer, PlaceCreateUpdateSerializer
from .filters import PlaceFilter
from src.apps.common.paginations import CustomPagination
from ...apps.common.permissions import IsEntrepreneur, IsAdmin
from .task import process_telegram_image


@method_decorator(queries_counter, name='dispatch')
@extend_schema(tags=["Place"])
class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdmin | IsEntrepreneur]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PlaceCreateUpdateSerializer
        return PlaceSerializer

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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        place_instance = serializer.save(user=self.request.user)

        file_id = request.data.get('image')
        is_telegram_upload = file_id and isinstance(file_id, str)

        if is_telegram_upload:
            process_telegram_image.delay(place_id=place_instance.id, file_id=file_id)

        read_serializer = PlaceSerializer(place_instance, context={'request': request})
        headers = self.get_success_headers(read_serializer.data)

        status_code = status.HTTP_202_ACCEPTED if is_telegram_upload else status.HTTP_201_CREATED

        return Response(read_serializer.data, status=status_code, headers=headers)
