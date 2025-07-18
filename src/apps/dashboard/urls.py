from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_dashboard_view, name='main_dashboard'),

    path('api/daily-search-stats/', views.api_daily_search_stats, name='api_daily_search_stats'),
    path('api/active-users-data/', views.api_active_users_data, name='api_active_users_data'),
    path('api/by-category/', views.api_category_pie_data, name='api_category_pie_data'),
    path('api/monthly-stats-data/', views.api_monthly_stats_data, name='api_monthly_stats_data'),
    path('api/search-history-log/', views.api_search_history_log, name='search-history-log')
]
