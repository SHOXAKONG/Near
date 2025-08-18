import logging
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
from src.apps.common.pagination import CustomPagination
from src.apps.common.permissions import IsEntrepreneur, IsAdmin
from .task import process_telegram_image

# Setup logger
logger = logging.getLogger(__name__)


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

                logger.info(f"[Place] User {self.request.user} requested nearby places "
                            f"from location (lat={lat}, lon={lon})")
            except (ValueError, TypeError):
                logger.warning(f"[Place] User {self.request.user} provided invalid coordinates: "
                               f"lat={latitude}, lon={longitude}")
                return Place.objects.none()
        else:
            logger.info(f"[Place] User {self.request.user} requested all places")

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        place_instance = serializer.save(user=self.request.user)

        file_id = request.data.get('image')
        is_telegram_upload = file_id and isinstance(file_id, str)

        if is_telegram_upload:
            logger.info(f"[Place] User {request.user} created place {place_instance.id} "
                        f"with Telegram image {file_id} (async processing started)")
            process_telegram_image.delay(place_id=place_instance.id, file_id=file_id)
        else:
            logger.info(f"[Place] User {request.user} created place {place_instance.id} "
                        f"with regular image upload")

        read_serializer = PlaceSerializer(place_instance, context={'request': request})
        headers = self.get_success_headers(read_serializer.data)

        status_code = status.HTTP_202_ACCEPTED if is_telegram_upload else status.HTTP_201_CREATED

        return Response(read_serializer.data, status=status_code, headers=headers)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        logger.info(f"[Place] User {request.user} updated place {kwargs.get('pk')}")
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        logger.info(f"[Place] User {request.user} partially updated place {kwargs.get('pk')}")
        return response

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"[Place] User {request.user} deleted place {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)
