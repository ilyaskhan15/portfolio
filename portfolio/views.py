from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from .models import Project, Skill, Experience, Education, Profile


class PortfolioView(TemplateView):
    """Main portfolio page"""
    template_name = 'portfolio/portfolio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.filter(is_active=True).first()
        except Profile.DoesNotExist:
            context['profile'] = None
            
        context['featured_projects'] = Project.objects.filter(
            is_featured=True, 
            status='published'
        ).order_by('order')[:6]
        
        context['featured_skills'] = Skill.objects.filter(
            is_featured=True
        ).order_by('order')[:8]
        
        context['recent_experiences'] = Experience.objects.filter(
            is_current=True
        ).order_by('order')[:3]
        
        return context


class ProjectDetailView(DetailView):
    """Individual project detail page"""
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(status='published').prefetch_related('technologies')


class SkillsView(ListView):
    """Skills showcase page"""
    model = Skill
    template_name = 'portfolio/skills.html'
    context_object_name = 'skills'
    
    def get_queryset(self):
        return Skill.objects.all().order_by('skill_type', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group skills by type
        skills_by_type = {}
        for skill in context['skills']:
            skill_type = skill.get_skill_type_display()
            if skill_type not in skills_by_type:
                skills_by_type[skill_type] = []
            skills_by_type[skill_type].append(skill)
        
        context['skills_by_type'] = skills_by_type
        return context


class ExperienceView(TemplateView):
    """Experience and education page"""
    template_name = 'portfolio/experience.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all().order_by('order')
        context['education'] = Education.objects.all().order_by('order')
        return context


class ResumeDownloadView(TemplateView):
    """Handle resume/CV download"""
    template_name = 'portfolio/resume_not_found.html'
    
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.filter(is_active=True).first()
            if profile and profile.resume:
                file_path = profile.resume.path
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file.read(), content_type='application/pdf')
                        response['Content-Disposition'] = f'attachment; filename="{profile.full_name}_Resume.pdf"'
                        return response
        except Exception as e:
            # Log the error for debugging
            print(f"Resume download error: {e}")
        
        # If no resume is found, render a template instead of raising 404
        return self.render_to_response(self.get_context_data())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        return context
