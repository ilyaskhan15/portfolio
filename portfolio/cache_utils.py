# ADVANCED CACHING UTILITIES
# Create this as portfolio/cache_utils.py

from django.core.cache import cache
from django.utils import timezone
from functools import wraps
import hashlib
import json


class CacheManager:
    """Advanced cache management utilities"""
    
    TIMEOUTS = {
        'homepage': 900,        # 15 minutes
        'portfolio': 1800,      # 30 minutes  
        'projects': 3600,       # 1 hour
        'skills': 1800,         # 30 minutes
        'blog_posts': 300,      # 5 minutes
        'static_pages': 3600,   # 1 hour
    }
    
    @staticmethod
    def get_cache_key(*args, **kwargs):
        """Generate consistent cache keys"""
        key_data = {
            'args': args,
            'kwargs': kwargs,
            'timestamp': timezone.now().strftime('%Y%m%d%H')  # Hour-based versioning
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    @classmethod
    def cached_query(cls, cache_type, key_suffix=''):
        """Decorator for caching database queries"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{cache_type}_{key_suffix}_{cls.get_cache_key(*args, **kwargs)}"
                result = cache.get(cache_key)
                
                if result is None:
                    result = func(*args, **kwargs)
                    timeout = cls.TIMEOUTS.get(cache_type, 900)
                    cache.set(cache_key, result, timeout)
                
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def invalidate_cache(patterns):
        """Invalidate multiple cache keys by pattern"""
        if isinstance(patterns, str):
            patterns = [patterns]
        
        cache.delete_many(patterns)
    
    @staticmethod
    def warm_cache():
        """Pre-populate frequently accessed cache entries"""
        from .models import Profile, Project, Skill
        
        # Warm up homepage data
        try:
            profile = Profile.objects.filter(is_active=True).first()
            latest_project = Project.objects.filter(
                status='published'
            ).order_by('-created_at').first()
            featured_skills = list(Skill.objects.filter(
                is_featured=True
            ).order_by('order')[:6])
            
            cache.set('homepage_data', {
                'profile': profile,
                'latest_project': latest_project,
                'featured_skills': featured_skills,
            }, 900)
            
            return True
        except Exception as e:
            print(f"Cache warming failed: {e}")
            return False


def cache_page_conditional(timeout, condition=None):
    """Cache page only if condition is met"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if condition and not condition(request):
                return view_func(request, *args, **kwargs)
            
            # Generate cache key based on request
            cache_key = f"page_{request.path}_{request.GET.urlencode()}"
            response = cache.get(cache_key)
            
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator


# Template fragment caching utility
def get_fragment_cache_key(fragment_name, *args):
    """Generate cache key for template fragments"""
    key_parts = [fragment_name] + [str(arg) for arg in args]
    return '_'.join(key_parts)


# Example usage in templates:
"""
<!-- Cache project list for 30 minutes -->
{% load cache %}
{% cache 1800 project_list %}
    {% for project in projects %}
        <div class="project-card">{{ project.title }}</div>
    {% endfor %}
{% endcache %}

<!-- Cache skill badges for 1 hour -->
{% cache 3600 skill_badges skill.id %}
    <div class="skill-badge">{{ skill.name }}</div>
{% endcache %}
"""