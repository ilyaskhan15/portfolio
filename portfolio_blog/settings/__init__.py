import os

# Use production settings by default, fall back to development
DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings.production')

if 'development' in DJANGO_SETTINGS_MODULE:
    from .development import *
else:
    from .production import *