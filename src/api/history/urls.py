from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SearchHistoryViewSet

router = DefaultRouter()

router.register('search-history', SearchHistoryViewSet, basename='search-history')

urlpatterns = [
    path('', include(router.urls))
]