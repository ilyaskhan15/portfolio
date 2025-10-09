# OPTIMIZED MODELS - Add these improvements to your models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.core.cache import cache
from PIL import Image
import os


class OptimizedSkill(models.Model):
    """Optimized Skill model with better indexing"""
    
    SKILL_TYPES = [
        ('technical', 'Technical'),
        ('framework', 'Framework'),
        ('tool', 'Tool'),
        ('language', 'Programming Language'),
        ('soft', 'Soft Skill'),
        ('other', 'Other'),
    ]
    
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=100, db_index=True)  # Added index
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES, default='technical', db_index=True)  # Added index
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='intermediate')
    description = models.TextField(max_length=500, blank=True)
    icon = models.ImageField(upload_to='portfolio/skills/', blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    is_featured = models.BooleanField(default=False, help_text="Display prominently on portfolio", db_index=True)  # Added index
    order = models.PositiveIntegerField(default=0, help_text="Display order", db_index=True)  # Added index
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['is_featured', 'order']),  # Composite index for featured skills
            models.Index(fields=['skill_type', 'order']),   # Composite index for grouping
        ]

    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear related caches
        cache.delete_many([
            'homepage_data',
            'skills_grouped',
            'featured_skills',
        ])


class OptimizedProject(models.Model):
    """Optimized Project model with better indexing and caching"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    PROJECT_TYPES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile Application'),
        ('desktop', 'Desktop Application'),
        ('api', 'API/Backend'),
        ('data', 'Data Science/Analysis'),
        ('ml', 'Machine Learning'),
        ('game', 'Game Development'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, db_index=True)  # Added index
    slug = models.SlugField(max_length=200, unique=True, blank=True, db_index=True)  # Explicit index
    short_description = models.CharField(max_length=255, help_text="Brief one-liner description")
    description = models.TextField(help_text="Detailed project description")
    
    # Project Details
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='web', db_index=True)  # Added index
    technologies = models.ManyToManyField('Skill', blank=True, related_name='projects')
    
    # Media
    featured_image = models.ImageField(
        upload_to='portfolio/projects/%Y/%m/',
        help_text="Main project screenshot (recommended: 1200x800px)",
        blank=True,
        null=True
    )
    featured_image_alt = models.CharField(max_length=255, blank=True)
    
    # Project Status and Dates
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published', db_index=True)  # Added index
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank for ongoing projects")
    
    # Portfolio Settings
    is_featured = models.BooleanField(default=False, help_text="Display prominently on portfolio", db_index=True)  # Added index
    order = models.PositiveIntegerField(default=0, help_text="Display order", db_index=True)  # Added index
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Added index for ordering
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),    # For published projects
            models.Index(fields=['is_featured', 'order']),     # For featured projects
            models.Index(fields=['project_type', '-created_at']),  # For filtering by type
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Ensure slug is unique
        original_slug = self.slug
        counter = 1
        while OptimizedProject.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
            
        if not self.meta_description:
            self.meta_description = self.short_description[:160]
            
        super().save(*args, **kwargs)
        
        # Clear related caches
        cache.delete_many([
            'homepage_data',
            f'project_detail_{self.slug}',
            'featured_projects',
        ])

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})


# Database connection optimization settings for production.py
DATABASE_OPTIMIZATION_SETTINGS = """
# Add these to your production.py for better database performance

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='postgres://localhost/portfolio_blog'),
        conn_max_age=600,  # Keep connections alive for 10 minutes
        conn_health_checks=True,  # Enable connection health checks
        ssl_require=config('DB_SSL_REQUIRE', default=True, cast=bool),
        options={
            'MAX_CONNS': 20,  # Maximum database connections
            'MIN_CONNS': 5,   # Minimum database connections
        }
    )
}

# Database query optimization
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Enable query analysis in development (add to your settings)
# if DEBUG:
#     LOGGING['loggers']['django.db.backends'] = {
#         'level': 'DEBUG',
#         'handlers': ['console'],
#     }
"""

# Example usage notes
OPTIMIZATION_NOTES = """
These are optimized model examples. To use:

1. Add the Meta classes with indexes to your existing models
2. Run: python manage.py makemigrations
3. Run: python manage.py migrate
4. Monitor query performance with django-debug-toolbar
"""