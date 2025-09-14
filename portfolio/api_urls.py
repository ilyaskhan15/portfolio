from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'projects', api_views.ProjectViewSet)
router.register(r'skills', api_views.SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]