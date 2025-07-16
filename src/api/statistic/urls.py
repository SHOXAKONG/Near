from rest_framework.routers import DefaultRouter
from .views import SearchHistoryStatViewSet, ActiveUserStatViewSet, DailySearchStatViewSet, MonthlyStatViewSet, \
    UsersListViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('statistics/search-history', SearchHistoryStatViewSet, basename='search-history-stats')
router.register('statistics/active-users', ActiveUserStatViewSet, basename='active-users-stats')
router.register('statistics/daily-search', DailySearchStatViewSet, basename='daily-search')
router.register('statistics/monthly-search', MonthlyStatViewSet, basename='monthly-search')
router.register('statistics/users-list', UsersListViewSet, basename='users-list')

urlpatterns = [
    path('', include(router.urls))
]
