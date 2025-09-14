#!/bin/bash

# Portfolio Blog Django Application Runner
# This script helps you run the Django development server

# Activate virtual environment
source enviroment/bin/activate

# Check if we need to run migrations
echo "Checking for pending migrations..."
python manage.py showmigrations --plan | grep -q '\[ \]'
if [ $? -eq 0 ]; then
    echo "Running pending migrations..."
    python manage.py migrate
fi

# Collect static files for production
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the development server
echo "Starting Django development server..."
echo "Access your site at: http://127.0.0.1:8000"
echo "Admin panel at: http://127.0.0.1:8000/admin"
echo ""
python manage.py runserver