from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.apps.common.permissions import IsAuthenticatedAndHasRole, IsAdmin, IsUser, IsEntrepreneur
from src.apps.place.utils import nearby_filter
from src.apps.common.paginations import CustomPagination
from src.api.place.serializers import PlaceSerializer
from src.apps.place.models import Place

@extend_schema(tags=["Place"])
class PlaceViewSets(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsEntrepreneur | IsUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'subcategory']
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'], url_path='nearby', permission_classes=[IsUser])
    def filter_near_place(self, request):
        user_latitude = request.query_params.get('latitude')
        user_longitude = request.query_params.get('longitude')

        if not user_latitude or not user_longitude:
            return Response({"error": "Latitude and longitude are required."}, status=status.HTTP_400_BAD_REQUEST)

        nearby_places = nearby_filter(user_latitude, user_longitude, Place.objects.all())
        return Response(nearby_places, status.HTTP_200_OK)
