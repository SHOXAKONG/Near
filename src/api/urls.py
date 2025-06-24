from django.urls import include, path

urlpatterns = [
    path('auth/', include('src.api.users.urls')),
    path('place/', include('src.api.place.urls')),
    path('category/', include('src.api.category.urls'))
]