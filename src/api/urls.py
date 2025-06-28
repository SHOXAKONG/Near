from django.urls import include, path

urlpatterns = [
    path('auth/', include('src.api.users.urls')),
    path('', include('src.api.place.urls')),
    path('', include('src.api.category.urls')),
    path('chat/', include('src.api.chat.urls'))
]