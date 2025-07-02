from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()

router.register('place', views.PlaceViewSet, basename='place')

urlpatterns = [
    path('', include(router.urls))
]
