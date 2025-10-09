# OPTIMIZED HEROKU CONFIGURATION
# Enhanced configuration for better performance on Heroku

# Procfile content - Replace your current Procfile with:
"""
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn portfolio_blog.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class gevent --worker-connections 1000 --max-requests 1000 --max-requests-jitter 50 --timeout 30
worker: celery -A portfolio_blog worker --loglevel=info --concurrency=2
"""

# Gunicorn configuration - create gunicorn.conf.py
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
backlog = 2048

# Worker processes
workers = min(4, (multiprocessing.cpu_count() * 2) + 1)
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, with up to 50 requests variation
max_requests = 1000
max_requests_jitter = 50

# Log to stdout
errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "portfolio_blog"

# Server mechanics
preload_app = True
daemon = False
pidfile = None
tmp_upload_dir = None

# SSL
forwarded_allow_ips = "*"
secure_scheme_headers = {"X-FORWARDED-PROTOCOL": "ssl", "X-FORWARDED-PROTO": "https", "X-FORWARDED-SSL": "on"}

# Performance tuning
worker_tmp_dir = "/dev/shm"  # Use in-memory filesystem for better performance