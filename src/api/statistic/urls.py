from rest_framework.routers import DefaultRouter
from .views import SearchHistoryStatViewSet, ActiveUserStatViewSet, DailySearchStatViewSet, MonthlyStatViewSet, \
    UserSearchHistoryViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'statistics/by-category', SearchHistoryStatViewSet, basename='search-stats-by-category')
router.register(r'statistics/active-users', ActiveUserStatViewSet, basename='active-users-stats')
router.register(r'statistics/daily-searches', DailySearchStatViewSet, basename='daily-search-stats')
router.register(r'statistics/monthly-summary', MonthlyStatViewSet, basename='monthly-stats')
router.register(r'statistics/search-history-users', UserSearchHistoryViewSet, basename='search-history-users')

urlpatterns = [
    path('', include(router.urls))
]
