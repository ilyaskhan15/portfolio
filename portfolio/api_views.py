from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Skill, Experience, Education, Profile
from .serializers import (
    ProjectSerializer, SkillSerializer, ExperienceSerializer, 
    EducationSerializer, ProfileSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """API viewset for portfolio projects"""
    queryset = Project.objects.filter(status='published').prefetch_related('technologies')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project_type', 'technologies', 'is_featured']
    search_fields = ['title', 'short_description', 'description']
    ordering_fields = ['created_at', 'order']
    ordering = ['order', '-created_at']
    lookup_field = 'slug'


class SkillViewSet(viewsets.ModelViewSet):
    """API viewset for skills"""
    queryset = Skill.objects.all().order_by('order')
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['skill_type', 'proficiency', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'years_experience']
    ordering = ['order', 'name']


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for work experience"""
    queryset = Experience.objects.all().order_by('order')
    serializer_class = ExperienceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employment_type', 'is_current']
    ordering_fields = ['start_date', 'order']
    ordering = ['order', '-start_date']


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for education"""
    queryset = Education.objects.all().order_by('order')
    serializer_class = EducationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['degree_type', 'is_current']
    ordering_fields = ['start_date', 'order']
    ordering = ['order', '-start_date']


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for profile"""
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer