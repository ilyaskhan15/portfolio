#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Upgrade pip first
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run collectstatic
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Create cache table (optional, for database cache)
echo "Creating cache table..."
python manage.py createcachetable || echo "Cache table creation failed, continuing..."

echo "Build process completed!"