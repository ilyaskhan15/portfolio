# OPTIMIZED VIEWS - Replace your current views.py with these optimizations

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Prefetch, Count, Q
from django.contrib.auth import get_user_model
import os
import mimetypes
import urllib.parse
from .models import Project, Skill, Experience, Education, Profile

User = get_user_model()


class OptimizedHomeView(TemplateView):
    """Optimized homepage with efficient queries and caching"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Use cache for frequently accessed data
        cache_key = 'homepage_data'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            # Efficient single query for profile
            profile = Profile.objects.filter(is_active=True).first()
            
            # Optimized project query with select_related for technologies
            latest_project = Project.objects.select_related().prefetch_related(
                'technologies'
            ).filter(status='published').order_by('-created_at').first()
            
            # Featured skills with single query
            featured_skills = list(Skill.objects.filter(
                is_featured=True
            ).order_by('order')[:6])
            
            cached_data = {
                'profile': profile,
                'latest_project': latest_project,
                'featured_skills': featured_skills,
            }
            
            # Cache for 15 minutes
            cache.set(cache_key, cached_data, 900)
        
        context.update(cached_data)
        
        # Blog posts (separate cache with shorter TTL)
        blog_cache_key = 'homepage_blog_posts'
        blog_data = cache.get(blog_cache_key)
        
        if blog_data is None:
            from blog.models import Post
            
            # Single query with select_related for author and category
            latest_posts = list(Post.objects.select_related(
                'author', 'category'
            ).filter(status='published').order_by('-published_at')[:3])
            
            blog_data = {
                'latest_football_post': next((p for p in latest_posts if p.category and p.category.name.lower() == 'football'), None),
                'latest_tech_posts': [p for p in latest_posts if not (p.category and p.category.name.lower() == 'football')][:2]
            }
            
            # Cache blog data for 5 minutes (more dynamic content)
            cache.set(blog_cache_key, blog_data, 300)
        
        context.update(blog_data)
        return context


class OptimizedPortfolioView(TemplateView):
    """Optimized portfolio page with efficient queries"""
    template_name = 'portfolio/portfolio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Single query for profile
        context['profile'] = Profile.objects.filter(is_active=True).first()
        
        # Optimized queries with prefetch_related
        context['featured_projects'] = Project.objects.prefetch_related(
            'technologies'
        ).filter(
            is_featured=True, 
            status='published'
        ).order_by('order')[:6]
        
        context['featured_skills'] = Skill.objects.filter(
            is_featured=True
        ).order_by('order')[:8]
        
        # Use prefetch_related for skills in experiences
        context['recent_experiences'] = Experience.objects.prefetch_related(
            'skills_used'
        ).filter(is_current=True).order_by('order')[:3]
        
        return context


class OptimizedProjectDetailView(DetailView):
    """Optimized project detail with all related data"""
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.select_related().prefetch_related(
            'technologies'
        ).filter(status='published')
    
    def get_object(self):
        """Cache individual project objects"""
        slug = self.kwargs.get('slug')
        cache_key = f'project_detail_{slug}'
        project = cache.get(cache_key)
        
        if project is None:
            project = get_object_or_404(self.get_queryset(), slug=slug)
            # Cache for 1 hour
            cache.set(cache_key, project, 3600)
        
        return project


class OptimizedSkillsView(ListView):
    """Optimized skills page with grouped display"""
    model = Skill
    template_name = 'portfolio/skills.html'
    context_object_name = 'skills'
    
    def get_queryset(self):
        # Single query, ordered for efficient grouping
        return Skill.objects.all().order_by('skill_type', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Cache grouped skills
        cache_key = 'skills_grouped'
        skills_by_type = cache.get(cache_key)
        
        if skills_by_type is None:
            skills_by_type = {}
            for skill in context['skills']:
                skill_type = skill.get_skill_type_display()
                if skill_type not in skills_by_type:
                    skills_by_type[skill_type] = []
                skills_by_type[skill_type].append(skill)
            
            # Cache for 30 minutes
            cache.set(cache_key, skills_by_type, 1800)
        
        context['skills_by_type'] = skills_by_type
        return context


# Add cache decorators to static views
@cache_page(60 * 30)  # Cache for 30 minutes
class AboutView(TemplateView):
    """Cached About page"""
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        return context


@cache_page(60 * 60)  # Cache for 1 hour
class ContactView(TemplateView):
    """Cached Contact page"""
    template_name = 'portfolio/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        return context


# Keep your existing views for compatibility
from .views import (
    create_users, ExperienceView, PrivacyView, 
    TermsView, ResumeDownloadView
)