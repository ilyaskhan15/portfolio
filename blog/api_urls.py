from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'posts', api_views.PostViewSet)
router.register(r'categories', api_views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]