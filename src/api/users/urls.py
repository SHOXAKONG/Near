from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()

router.register('register', views.RegisterViewSet, 'register')
router.register('confirm', views.ConfirmViewSet, 'confirm')
urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
