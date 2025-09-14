#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Run collectstatic
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Create cache table (optional, for database cache)
python manage.py createcachetable