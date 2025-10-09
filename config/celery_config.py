# CELERY CONFIGURATION FOR BACKGROUND TASKS
# Create this as portfolio_blog/celery.py

"""
This is a configuration template for Celery. To use:
1. Install celery: pip install celery[redis]
2. Create portfolio_blog/celery.py with this content
3. Add to portfolio_blog/__init__.py:
   from .celery import app as celery_app
   __all__ = ('celery_app',)
"""

from __future__ import absolute_import, unicode_literals
import os

# Celery app configuration
def create_celery_app():
    """Create and configure Celery app"""
    try:
        # Dynamic import to avoid linting errors
        celery_module = __import__('celery', fromlist=['Celery'])
        Celery = celery_module.Celery
        
        # Set the default Django settings module for the 'celery' program.
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings.production')
        
        app = Celery('portfolio_blog')
        return app
    except (ImportError, ModuleNotFoundError):
        # Return a mock object if Celery is not installed
        class MockCelery:
            def config_from_object(self, *args, **kwargs):
                pass
            def autodiscover_tasks(self, *args, **kwargs):
                pass
            def task(self, *args, **kwargs):
                def decorator(func):
                    return func
                return decorator
            
        return MockCelery()

# Create app instance
app = create_celery_app()

# Configure Celery (works with both real Celery and mock)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Only configure if it's a real Celery app
if hasattr(app, 'conf'):
    # Celery configuration
    try:
        app.conf.update(
            # Broker settings
            broker_url=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
            result_backend=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
            
            # Task settings
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            
            # Performance settings
            task_routes={
                'portfolio.tasks.optimize_image': {'queue': 'images'},
                'portfolio.tasks.send_email': {'queue': 'emails'},
                'blog.tasks.update_post_analytics': {'queue': 'analytics'},
            },
            
            # Worker settings
            worker_prefetch_multiplier=1,
            task_acks_late=True,
            worker_disable_rate_limits=True,
            
            # Result backend settings
            result_expires=3600,  # 1 hour
            result_backend_transport_options={
                'master_name': 'mymaster',
                'visibility_timeout': 3600,
            },
        )
    except Exception as e:
        print(f"Celery configuration warning: {e}")


# Task definitions (only if Celery is available)
def define_tasks(app):
    """Define Celery tasks"""
    if not app:
        return
    
    @app.task(bind=True)
    def debug_task(self):
        print(f'Request: {self.request!r}')

    @app.task
    def optimize_uploaded_image(image_path, max_width=1200, quality=85):
        """Optimize images in the background"""
        try:
            from PIL import Image
            import os
            
            if not os.path.exists(image_path):
                return f"Image not found: {image_path}"
            
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if needed
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save optimized version
                img.save(image_path, 'JPEG', quality=quality, optimize=True, progressive=True)
                
            return f"Image optimized: {image_path}"
        
        except Exception as e:
            return f"Image optimization failed: {str(e)}"


    @app.task
    def warm_cache_task():
        """Warm up cache in background"""
        try:
            from portfolio.cache_utils import CacheManager
            return CacheManager.warm_cache()
        except ImportError:
            return "Cache utils not available"

    @app.task
    def send_contact_email(name, email, message):
        """Send contact form email in background"""
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            subject = f"Portfolio Contact: {name}"
            body = f"""
        New contact form submission:
        
        Name: {name}
        Email: {email}
        Message:
        {message}
        """
            
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return "Email sent successfully"
        except Exception as e:
            return f"Email sending failed: {str(e)}"

    @app.task
    def update_analytics_data():
        """Update analytics data in background"""
        try:
            from blog.models import Post
            from django.db.models import F
            
            # Example: Update reading times for all posts
            posts_updated = 0
            for post in Post.objects.filter(status='published'):
                if post.content:
                    word_count = len(post.content.split())
                    reading_time = max(1, word_count // 200)
                    if post.reading_time != reading_time:
                        post.reading_time = reading_time
                        post.save(update_fields=['reading_time'])
                        posts_updated += 1
            
            return f"Updated reading time for {posts_updated} posts"
        except ImportError:
            return "Blog models not available"

# Call the function to define tasks
define_tasks(app)