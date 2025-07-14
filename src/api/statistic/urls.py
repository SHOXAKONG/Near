from rest_framework.routers import DefaultRouter
from .views import SearchHistoryStatViewSet, ActiveUserStatViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('statistics/search-history', SearchHistoryStatViewSet, basename='search-history-stats')
router.register('statistics/active-users', ActiveUserStatViewSet, basename='active-users-stats')

urlpatterns = [
    path('', include(router.urls))
]
