# Heroku Environment Variables Setup

This document lists all the environment variables you need to set in your Heroku app for deployment.

## Required Environment Variables

### Django Configuration
```bash
# Django Settings Module (Important!)
DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production

# Security
SECRET_KEY=your-secret-key-here-generate-new-one-for-production
DEBUG=False

# Database URL (Heroku PostgreSQL addon will set this automatically)
DATABASE_URL=postgres://username:password@hostname:port/database_name
```

### Hosting Configuration
```bash
# Allowed Hosts (Update with your Heroku app name)
ALLOWED_HOSTS=your-app-name.herokuapp.com,your-custom-domain.com

# CSRF Trusted Origins (Update with your domains)
CSRF_TRUSTED_ORIGINS=https://your-app-name.herokuapp.com,https://your-custom-domain.com
```

### Cloudinary (Media Files)
```bash
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### Email Configuration (Optional)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### CORS Settings (Optional - if you have a frontend)
```bash
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## How to Set Environment Variables in Heroku

### Method 1: Using Heroku CLI
```bash
heroku config:set DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-cloudinary-api-key
heroku config:set CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### Method 2: Using Heroku Dashboard
1. Go to your app dashboard on heroku.com
2. Click on "Settings" tab
3. Click "Reveal Config Vars"
4. Add each variable name and value

## Important Notes

1. **Generate a new SECRET_KEY** for production. You can use Django's built-in utility:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Database**: Heroku will automatically set `DATABASE_URL` when you add a PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. **Static Files**: Already configured with WhiteNoise - no additional setup needed.

4. **Media Files**: Using Cloudinary for media file storage - make sure to configure the Cloudinary variables.

5. **Custom Domain**: If using a custom domain, add it to both `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

## Deployment Commands

After setting up environment variables:

```bash
# Deploy to Heroku
git add .
git commit -m "Ready for Heroku deployment"
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Collect static files (if needed)
heroku run python manage.py collectstatic --noinput

# Create superuser (optional)
heroku run python manage.py createsuperuser
```