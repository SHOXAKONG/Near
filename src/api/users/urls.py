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
router.register('forgot_password', views.ForgotPasswordViewSet, 'forgot_password')
router.register('restore_password', views.RestorePasswordViewSet, 'retore_password')
router.register('users', views.UserViewSet, 'users')
router.register('', views.LogoutViewSet, 'logout')
router.register('users-data', views.GetUserDataViewSet, 'users-data')
urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('become-entrepreneur/', views.BecomeEntrepreneurAPIView.as_view(), name='become-entrepreneur')
]
