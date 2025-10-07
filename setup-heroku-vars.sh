#!/bin/bash

# Heroku Environment Variables Configuration Script
# Run this script to set all necessary environment variables for your Heroku app

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[INPUT REQUIRED]${NC} $1"
}

echo "🔧 Heroku Environment Variables Configuration"
echo "============================================="

# Check if Heroku app is configured
if ! heroku apps:info &> /dev/null; then
    echo "Please run this script from your project directory with Heroku app configured."
    echo "Or specify app name: heroku config:set VARIABLE=value -a your-app-name"
    exit 1
fi

APP_NAME=$(heroku apps:info | grep "=== " | cut -d' ' -f2)
print_status "Configuring environment variables for app: $APP_NAME"

# Essential Django Configuration
print_status "Setting essential Django configuration..."
heroku config:set DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production
heroku config:set DEBUG=False

# Generate and set secret key
print_status "Generating new SECRET_KEY..."
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set SECRET_KEY="$SECRET_KEY"
print_success "SECRET_KEY generated and set"

# Get app URL for allowed hosts
APP_URL=$(heroku info -s | grep web_url | cut -d= -f2 | sed 's|https://||' | sed 's|/||')
print_status "Setting ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS..."

print_warning "Enter your custom domain (optional, press Enter to skip):"
read -r CUSTOM_DOMAIN

if [ -n "$CUSTOM_DOMAIN" ]; then
    ALLOWED_HOSTS="$APP_URL,$CUSTOM_DOMAIN,www.$CUSTOM_DOMAIN"
    CSRF_ORIGINS="https://$APP_URL,https://$CUSTOM_DOMAIN,https://www.$CUSTOM_DOMAIN"
else
    ALLOWED_HOSTS="$APP_URL"
    CSRF_ORIGINS="https://$APP_URL"
fi

heroku config:set ALLOWED_HOSTS="$ALLOWED_HOSTS"
heroku config:set CSRF_TRUSTED_ORIGINS="$CSRF_ORIGINS"
print_success "Allowed hosts configured"

# Cloudinary Configuration
echo ""
print_warning "Cloudinary Configuration Required"
echo "Please get your Cloudinary credentials from: https://cloudinary.com/console"
echo ""

print_warning "Enter your Cloudinary Cloud Name:"
read -r CLOUD_NAME
print_warning "Enter your Cloudinary API Key:"
read -r API_KEY
print_warning "Enter your Cloudinary API Secret:"
read -s API_SECRET
echo ""

if [ -n "$CLOUD_NAME" ] && [ -n "$API_KEY" ] && [ -n "$API_SECRET" ]; then
    heroku config:set CLOUDINARY_CLOUD_NAME="$CLOUD_NAME"
    heroku config:set CLOUDINARY_API_KEY="$API_KEY"
    heroku config:set CLOUDINARY_API_SECRET="$API_SECRET"
    print_success "Cloudinary configuration set"
else
    print_warning "Cloudinary configuration skipped - you can set it later with:"
    echo "heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name"
    echo "heroku config:set CLOUDINARY_API_KEY=your-api-key"
    echo "heroku config:set CLOUDINARY_API_SECRET=your-api-secret"
fi

# Email Configuration (Optional)
echo ""
print_warning "Email Configuration (Optional - for contact forms)"
echo "Press Enter to skip, or provide SMTP details:"
print_warning "Email Host (e.g., smtp.gmail.com):"
read -r EMAIL_HOST

if [ -n "$EMAIL_HOST" ]; then
    print_warning "Email Port (default: 587):"
    read -r EMAIL_PORT
    EMAIL_PORT=${EMAIL_PORT:-587}
    
    print_warning "Email Username:"
    read -r EMAIL_USER
    
    print_warning "Email Password (App Password for Gmail):"
    read -s EMAIL_PASSWORD
    echo ""
    
    heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    heroku config:set EMAIL_HOST="$EMAIL_HOST"
    heroku config:set EMAIL_PORT="$EMAIL_PORT"
    heroku config:set EMAIL_USE_TLS=True
    heroku config:set EMAIL_HOST_USER="$EMAIL_USER"
    heroku config:set EMAIL_HOST_PASSWORD="$EMAIL_PASSWORD"
    
    print_success "Email configuration set"
else
    print_status "Email configuration skipped"
fi

# Time Zone Configuration
print_warning "Time Zone (default: UTC):"
read -r TIMEZONE
TIMEZONE=${TIMEZONE:-UTC}
heroku config:set TIME_ZONE="$TIMEZONE"

# Display current configuration
echo ""
print_success "Environment variables configuration completed!"
echo ""
print_status "Current Heroku configuration:"
heroku config

echo ""
print_status "Next steps:"
echo "1. Deploy your application: git push heroku main"
echo "2. Run migrations: heroku run python manage.py migrate"
echo "3. Create superuser: heroku run python manage.py createsuperuser"
echo "4. Open your app: heroku open"

echo ""
print_success "Your Django app is ready for deployment! 🚀"