# FRONTEND OPTIMIZATION CONFIGURATION
# Add these settings to your production.py file

"""
To use these settings, add the following to your production.py:

from decouple import config
from pathlib import Path

# Enhanced WhiteNoise configuration for production.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files optimization
# STATICFILES_DIRS = [BASE_DIR / 'static']  # Uncomment if you have a static folder

# WhiteNoise settings for maximum performance
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 
    'bz2', 'tbz', 'xz', 'br', 'mp4', 'mp3', 'woff', 'woff2'
]
WHITENOISE_MAX_AGE = 31536000  # 1 year cache for static files

# Security headers for performance
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Add this to your MIDDLEWARE list:
# 'portfolio.middleware.PerformanceMiddleware',

# CDN Configuration (if using)
CDN_DOMAIN = config('CDN_DOMAIN', default='')
if CDN_DOMAIN:
    STATIC_URL = f'https://{CDN_DOMAIN}/static/'

# Image optimization settings for Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'), 
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    'MEDIA_TAG': 'portfolio',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
    'EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS': (),
    'OVERWRITE_ON_UPLOAD': True,
    'RESOURCE_OPTIONS': {
        'quality': 'auto:good',  # Automatic quality optimization
        'fetch_format': 'auto',   # Automatic format selection
        'flags': 'progressive',   # Progressive JPEG loading
    }
}
"""

# Configuration constants
LAZY_LOADING_THRESHOLD = 2  # Number of images to load immediately
LAZY_LOADING_PLACEHOLDER = '/static/img/placeholder.jpg'