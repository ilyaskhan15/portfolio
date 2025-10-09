# PERFORMANCE MIDDLEWARE
# Create this as portfolio/middleware.py

import time
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.cache import cache


class PerformanceMiddleware(MiddlewareMixin):
    """Middleware for performance optimization and monitoring"""
    
    def process_request(self, request):
        """Start timing the request"""
        request.start_time = time.time()
        
        # Set performance headers
        return None
    
    def process_response(self, request, response):
        """Add performance headers and optimization"""
        
        # Add timing header for development
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        # Add caching headers
        if request.method == 'GET' and response.status_code == 200:
            # Cache static pages longer
            if any(path in request.path for path in ['/about/', '/contact/', '/privacy/', '/terms/']):
                response['Cache-Control'] = 'public, max-age=3600'  # 1 hour
                response['Vary'] = 'Accept-Encoding'
            
            # Cache API responses shorter
            elif '/api/' in request.path:
                response['Cache-Control'] = 'public, max-age=300'   # 5 minutes
            
            # Cache portfolio pages moderately
            elif any(path in request.path for path in ['/portfolio/', '/projects/', '/skills/']):
                response['Cache-Control'] = 'public, max-age=1800'  # 30 minutes
        
        # Compression hints
        if 'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', ''):
            response['Vary'] = 'Accept-Encoding'
        
        # Security and performance headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Preload critical resources
        if request.path == '/':
            response['Link'] = (
                '</static/css/tailwind.min.css>; rel=preload; as=style, '
                '</static/js/main.js>; rel=preload; as=script'
            )
        
        return response


class CompressionMiddleware(MiddlewareMixin):
    """Middleware for response compression"""
    
    def process_response(self, request, response):
        """Add compression hints"""
        
        # Enable compression for text content
        content_type = response.get('Content-Type', '')
        
        if any(ct in content_type for ct in [
            'text/', 'application/json', 'application/javascript',
            'application/xml', 'image/svg+xml'
        ]):
            response['Vary'] = response.get('Vary', '') + ', Accept-Encoding'
        
        return response


class ImageOptimizationMiddleware(MiddlewareMixin):
    """Middleware for image optimization hints"""
    
    def process_response(self, request, response):
        """Add image optimization headers"""
        
        if 'text/html' in response.get('Content-Type', ''):
            # Add resource hints for better performance
            response['Link'] = response.get('Link', '') + (
                ', </static/img/hero-bg.webp>; rel=preload; as=image; '
                'type=image/webp'
            )
        
        return response