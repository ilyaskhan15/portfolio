from rest_framework import serializers
from .models import Project, Skill, Experience, Education, Profile


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skills"""
    proficiency_display = serializers.CharField(source='get_proficiency_display', read_only=True)
    skill_type_display = serializers.CharField(source='get_skill_type_display', read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'skill_type', 'skill_type_display', 'proficiency', 
            'proficiency_display', 'description', 'icon', 'years_experience', 
            'is_featured', 'order'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for portfolio projects"""
    technologies = SkillSerializer(many=True, read_only=True)
    project_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    duration = serializers.CharField(read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'project_type', 'project_type_display', 'technologies',
            'featured_image', 'featured_image_alt', 'image_1', 'image_2', 'image_3',
            'live_url', 'github_url', 'demo_url', 'status',
            'start_date', 'end_date', 'duration', 'is_ongoing',
            'is_featured', 'order', 'created_at', 'updated_at'
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for work experience"""
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    skills_used = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Experience
        fields = [
            'id', 'position', 'company', 'employment_type', 'employment_type_display',
            'location', 'start_date', 'end_date', 'description', 'skills_used',
            'is_current', 'order'
        ]


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for education"""
    degree_type_display = serializers.CharField(source='get_degree_type_display', read_only=True)
    
    class Meta:
        model = Education
        fields = [
            'id', 'institution', 'degree_type', 'degree_type_display',
            'field_of_study', 'start_date', 'end_date', 'grade',
            'description', 'is_current', 'order'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for personal profile"""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'title', 'bio',
            'email', 'phone', 'location', 'profile_image', 'resume',
            'website', 'linkedin', 'github', 'twitter', 'instagram',
            'meta_description', 'created_at', 'updated_at'
        ]