# REDIS CACHING CONFIGURATION
# Add these settings to your production.py file

"""
To use these settings, copy the relevant parts to your production.py:

import os
from decouple import config

# Redis Configuration for Caching
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
        'KEY_PREFIX': 'portfolio',
        'VERSION': 1,
        'TIMEOUT': 300,  # Default timeout: 5 minutes
    }
}

# Session storage in Redis for better performance
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Template caching - Update your TEMPLATES setting:
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Cache middleware - Add these to your MIDDLEWARE setting:
# Place 'django.middleware.cache.UpdateCacheMiddleware' at the top
# Place 'django.middleware.cache.FetchFromCacheMiddleware' at the bottom

# Cache settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'portfolio'
"""

# Custom cache timeout settings
CACHE_TIMEOUTS = {
    'homepage': 900,        # 15 minutes
    'portfolio': 1800,      # 30 minutes  
    'projects': 3600,       # 1 hour
    'skills': 1800,         # 30 minutes
    'blog_posts': 300,      # 5 minutes
    'static_pages': 3600,   # 1 hour
}