#!/bin/bash

# Heroku Deployment Script for Django Portfolio Blog
# This script helps automate the Heroku deployment process

set -e  # Exit on any error

echo "🚀 Starting Heroku deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    print_error "Heroku CLI is not installed. Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    print_warning "Not logged in to Heroku. Please run 'heroku login' first."
    exit 1
fi

print_success "Heroku CLI is installed and you are logged in."

# Check if we're in a git repository
if [ ! -d .git ]; then
    print_error "This directory is not a git repository. Please run 'git init' first."
    exit 1
fi

# Ask for app name if not provided
if [ -z "$1" ]; then
    read -p "Enter your Heroku app name (or press Enter for auto-generated name): " APP_NAME
else
    APP_NAME="$1"
fi

# Create Heroku app
print_status "Creating Heroku app..."
if [ -z "$APP_NAME" ]; then
    heroku create
else
    heroku create "$APP_NAME" || {
        print_warning "App name might already exist or be invalid. Continuing with existing app..."
        heroku git:remote -a "$APP_NAME"
    }
fi

# Add PostgreSQL addon
print_status "Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:essential-0 || heroku addons:create heroku-postgresql:mini || print_warning "PostgreSQL addon might already exist."

# Set essential environment variables
print_status "Setting essential environment variables..."

# Generate secret key
if [ -f "enviroment/bin/activate" ]; then
    source enviroment/bin/activate
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    deactivate
else
    # Fallback: generate a simple secret key without Django
    SECRET_KEY=$(openssl rand -hex 50)
fi
heroku config:set SECRET_KEY="$SECRET_KEY"

# Set Django settings module
heroku config:set DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production

# Set debug to false
heroku config:set DEBUG=False

# Get the app URL and set allowed hosts
APP_URL=$(heroku info -s | grep web_url | cut -d= -f2 | sed 's|https://||' | sed 's|/||')
if [ -n "$APP_URL" ]; then
    heroku config:set ALLOWED_HOSTS="$APP_URL"
    heroku config:set CSRF_TRUSTED_ORIGINS="https://$APP_URL"
    print_success "Set ALLOWED_HOSTS to: $APP_URL"
fi

# Prompt for Cloudinary credentials
print_warning "Please set up your Cloudinary credentials manually:"
echo "1. Sign up at https://cloudinary.com if you haven't already"
echo "2. Get your credentials from the Cloudinary dashboard"
echo "3. Run the following commands with your actual values:"
echo ""
echo "heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name"
echo "heroku config:set CLOUDINARY_API_KEY=your-api-key"
echo "heroku config:set CLOUDINARY_API_SECRET=your-api-secret"
echo ""

# Ask if user wants to continue with deployment
read -p "Have you set up Cloudinary credentials? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Please set up Cloudinary credentials and then run: git push heroku main"
    exit 0
fi

# Deploy to Heroku
print_status "Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku - $(date)" || print_warning "No changes to commit."
git push heroku main

# Check if deployment was successful
if [ $? -eq 0 ]; then
    print_success "Deployment completed successfully!"
    
    # Offer to create superuser
    read -p "Would you like to create a Django superuser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        heroku run python manage.py createsuperuser
    fi
    
    # Open the app
    read -p "Would you like to open your app in the browser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        heroku open
    fi
    
    print_success "Your Django app is now live on Heroku!"
    echo ""
    echo "Next steps:"
    echo "- Visit your app: $(heroku info -s | grep web_url | cut -d= -f2)"
    echo "- View logs: heroku logs --tail"
    echo "- Access admin: $(heroku info -s | grep web_url | cut -d= -f2)admin/"
    
else
    print_error "Deployment failed. Check the logs with: heroku logs --tail"
    exit 1
fi