from .base import *
import dj_database_url
import os

DEBUG = config('DEBUG', default=False, cast=bool)

# ✅ Allowed Hosts for Heroku + Custom Domain
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='muhammadilyas.herokuapp.com,muhammadilyas.tech,www.muhammadilyas.tech',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ✅ CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://muhammadilyas.herokuapp.com,https://muhammadilyas.tech,https://www.muhammadilyas.tech',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ✅ Database (Heroku auto-sets DATABASE_URL)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='postgres://localhost/portfolio_blog'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=config('DB_SSL_REQUIRE', default=True, cast=bool)
    )
}

# ✅ Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Override storage backends for production
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        # WhiteNoise with compression for production
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Legacy setting for compatibility
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files will use Cloudinary (configured in base.py)
# No need to set MEDIA_URL and MEDIA_ROOT here - Cloudinary handles it

# ✅ Security (HTTPS)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ✅ CORS (If needed)
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://muhammadilyas.tech,https://www.muhammadilyas.tech',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ✅ Site ID for django.contrib.sites
SITE_ID = 1

# ✅ Logging (Heroku-compatible - console only)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
