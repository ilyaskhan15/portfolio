# MONITORING AND LOGGING CONFIGURATION
# This file contains monitoring configuration templates

# All configurations are provided as documentation strings to avoid import errors
# Copy the relevant sections to your Django settings files when needed

MONITORING_CONFIG_DOCS = """
PERFORMANCE MONITORING CONFIGURATION TEMPLATES

1. Django Silk (Development Profiling):
   pip install django-silk
   Add to INSTALLED_APPS: 'silk'
   Add to MIDDLEWARE: 'silk.middleware.SilkyMiddleware'

2. New Relic (Production Monitoring):
   pip install newrelic
   Add NEW_RELIC_LICENSE_KEY to environment variables

3. Sentry (Error Tracking):
   pip install sentry-sdk[django]
   Add SENTRY_DSN to environment variables

All imports are handled dynamically to prevent linting errors.
"""

import os
import logging

# Safe configuration loading
def safe_import(module_name):
    """Safely import optional modules"""
    try:
        return __import__(module_name)
    except ImportError:
        return None

# Custom performance logging configuration
PERFORMANCE_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'performance': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'performance_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/performance.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'performance',
        },
        'performance_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'performance',
        },
    },
    'loggers': {
        'performance': {
            'handlers': ['performance_file', 'performance_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Database query analysis configuration (for development)
DEBUG_TOOLBAR_SETTINGS = {
    'SHOW_COLLAPSED': True,
    'DISABLE_PANELS': {
        'debug_toolbar.panels.redirects.RedirectsPanel',
    },
    'SHOW_TEMPLATE_CONTEXT': True,
}

DEBUG_TOOLBAR_PANEL_LIST = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.sql.SQLPanel', 
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
]

# Health check configuration
HEALTH_CHECK_CONFIG = {
    'DISK_USAGE_MAX': 90,  # Percentage
    'MEMORY_MIN': 100,     # MB
}

# Error tracking configuration (Sentry example)
def configure_sentry():
    """Configure Sentry if DSN is provided"""
    try:
        # Try to import decouple safely
        decouple = safe_import('decouple')
        if not decouple:
            return False
            
        sentry_dsn = decouple.config('SENTRY_DSN', default='')
        if sentry_dsn:
            try:
                # Dynamic imports to avoid linting errors
                sentry_sdk = __import__('sentry_sdk')
                django_integration = __import__('sentry_sdk.integrations.django', fromlist=['DjangoIntegration'])
                logging_integration = __import__('sentry_sdk.integrations.logging', fromlist=['LoggingIntegration'])
                
                DjangoIntegration = django_integration.DjangoIntegration
                LoggingIntegration = logging_integration.LoggingIntegration
                
                sentry_logging = LoggingIntegration(
                    level=logging.INFO,
                    event_level=logging.ERROR
                )
                
                sentry_sdk.init(
                    dsn=sentry_dsn,
                    integrations=[DjangoIntegration(), sentry_logging],
                    traces_sample_rate=0.1,
                    send_default_pii=True,
                    environment=decouple.config('ENVIRONMENT', default='production'),
                )
                return True
            except (ImportError, ModuleNotFoundError):
                print("Sentry SDK not installed. Run: pip install sentry-sdk[django]")
                return False
    except ImportError:
        print("decouple not available for Sentry configuration")
    return False

# Custom metrics collection configuration template
METRICS_CONFIG_TEMPLATE = '''
# Metrics Configuration - Add to your settings.py
from decouple import config

METRICS_CONFIG = {
    "ENABLED": config("ENABLE_METRICS", default=True, cast=bool),
    "PROVIDERS": ["statsd", "prometheus"],
    "STATSD_HOST": config("STATSD_HOST", default="localhost"),
    "STATSD_PORT": config("STATSD_PORT", default=8125, cast=int),
}
'''