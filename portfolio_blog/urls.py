"""
URL configuration for portfolio_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from portfolio.views import HomeView
import os

# View to serve ads.txt file
def serve_ads_txt(request):
    """Serve ads.txt file for Google AdSense.

    Looks in multiple locations to be robust across deployments:
    - STATIC_ROOT (if set, where collectstatic places files)
    - repository 'static/ads.txt'
    - 'staticfiles/ads.txt' (collected copy)
    """
    from django.http import FileResponse, Http404
    candidates = []
    # Check STATIC_ROOT first if available
    if getattr(settings, 'STATIC_ROOT', None):
        candidates.append(os.path.join(settings.STATIC_ROOT, 'ads.txt'))
    # Check repository static directory
    candidates.append(os.path.join(settings.BASE_DIR, 'static', 'ads.txt'))
    # Check collected staticfiles directory as fallback
    candidates.append(os.path.join(settings.BASE_DIR, 'staticfiles', 'ads.txt'))

    for path in candidates:
        if path and os.path.exists(path):
            return FileResponse(open(path, 'rb'), content_type='text/plain; charset=utf-8')

    raise Http404("ads.txt not found")

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Google AdSense ads.txt
    path('ads.txt', serve_ads_txt, name='ads_txt'),
    
    # Homepage - Dynamic content
    path('', HomeView.as_view(), name='home'),
    
    # Apps
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    
    # API
    path('api/', include('blog.api_urls')),
    path('api/portfolio/', include('portfolio.api_urls')),
    
    # Authentication
    path('accounts/', include('allauth.urls')),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production, serve media files via Django
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
