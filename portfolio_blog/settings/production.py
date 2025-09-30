from .base import *
import dj_database_url

DEBUG = False

# ✅ Allowed Hosts for Heroku + Custom Domain
ALLOWED_HOSTS = [
    'muhammadilyas.herokuapp.com',
    'muhammadilyas.tech',
    'www.muhammadilyas.tech',
]

# ✅ CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://muhammadilyas.herokuapp.com',
    'https://muhammadilyas.tech',
    'https://www.muhammadilyas.tech',
]

# ✅ Database (Heroku auto-sets DATABASE_URL)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# ✅ Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Security (HTTPS)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ✅ CORS (If needed)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://muhammadilyas.tech',
    'https://www.muhammadilyas.tech',
]

# ✅ Logging (Optional but safe)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
