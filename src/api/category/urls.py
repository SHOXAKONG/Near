from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()

router.register('', views.CategoryViewSet, 'category')
router.register('subcategory', views.SubcategoryVieSet, 'subcategory')
urlpatterns = [
    path('', include(router.urls))
]