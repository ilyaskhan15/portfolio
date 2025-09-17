#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Check Python version
echo "Python version being used:"
python --version

# Upgrade pip first
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies with explicit PostgreSQL adapter
echo "Installing Python dependencies..."
pip install psycopg2-binary>=2.9.0,<3.0
pip install -r requirements.txt

# Run collectstatic
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser automatically
echo "Creating admin users..."
python manage.py create_admin

# Create cache table (optional, for database cache)
echo "Creating cache table..."
python manage.py createcachetable || echo "Cache table creation failed, continuing..."

echo "Build process completed!"