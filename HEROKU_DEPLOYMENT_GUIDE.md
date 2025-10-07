# Heroku Deployment Guide

This guide will walk you through deploying your Django portfolio blog application to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Make sure your project is in a git repository
4. **Cloudinary Account**: Sign up at [cloudinary.com](https://cloudinary.com) for media file storage

## Step 1: Prepare Your Application

Your application is already configured for Heroku deployment with:
- ✅ `Procfile` with gunicorn and release commands
- ✅ `requirements.txt` with all necessary packages
- ✅ `runtime.txt` specifying Python version
- ✅ Production settings in `portfolio_blog/settings/production.py`
- ✅ WhiteNoise for static files
- ✅ Environment variable configuration

## Step 2: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app (replace 'your-app-name' with your desired name)
heroku create your-app-name

# Or if you want Heroku to generate a random name
heroku create
```

## Step 3: Add PostgreSQL Database

```bash
# Add PostgreSQL addon (free tier)
heroku addons:create heroku-postgresql:hobby-dev
```

## Step 4: Set Environment Variables

### Essential Variables (Required)
```bash
# Django configuration
heroku config:set DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set DEBUG=False

# Update with your actual Heroku app name
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set CSRF_TRUSTED_ORIGINS=https://your-app-name.herokuapp.com

# Cloudinary configuration (get these from your Cloudinary dashboard)
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-cloudinary-api-key
heroku config:set CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### Optional Variables
```bash
# Time zone (optional)
heroku config:set TIME_ZONE=UTC

# Email configuration (if you want contact forms to work)
heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password

# Security settings (optional - defaults are already secure)
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True
```

## Step 5: Deploy to Heroku

```bash
# Add Heroku remote (if not done automatically)
heroku git:remote -a your-app-name

# Deploy your application
git add .
git commit -m "Ready for Heroku deployment"
git push heroku main
```

## Step 6: Run Initial Setup Commands

```bash
# Create database tables (this happens automatically via release command in Procfile)
# But you can also run it manually:
heroku run python manage.py migrate

# Collect static files (optional - WhiteNoise handles this)
heroku run python manage.py collectstatic --noinput

# Create a superuser account
heroku run python manage.py createsuperuser
```

## Step 7: Open Your App

```bash
# Open your deployed application
heroku open

# Or visit: https://your-app-name.herokuapp.com
```

## Step 8: Configure Custom Domain (Optional)

If you have a custom domain:

```bash
# Add your custom domain to Heroku
heroku domains:add your-domain.com
heroku domains:add www.your-domain.com

# Update environment variables to include your custom domain
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com,your-domain.com,www.your-domain.com
heroku config:set CSRF_TRUSTED_ORIGINS=https://your-app-name.herokuapp.com,https://your-domain.com,https://www.your-domain.com
```

Then configure your DNS settings to point to Heroku (see Heroku documentation for details).

## Troubleshooting

### View Logs
```bash
# View recent logs
heroku logs --tail

# View specific number of log lines
heroku logs -n 200
```

### Common Issues

1. **Static files not loading**: Make sure `DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production` is set
2. **Database connection issues**: Verify PostgreSQL addon is installed with `heroku addons`
3. **Secret key errors**: Make sure `SECRET_KEY` environment variable is set
4. **Media files not uploading**: Check Cloudinary configuration variables

### Useful Commands
```bash
# Check environment variables
heroku config

# Restart the application
heroku restart

# Access Django shell
heroku run python manage.py shell

# Run custom management commands
heroku run python manage.py your_command
```

## Production Checklist

Before going live, make sure:
- [ ] All environment variables are set
- [ ] Database migrations have been run
- [ ] Superuser account is created
- [ ] Cloudinary is properly configured for media files
- [ ] Email configuration is set up (if using contact forms)
- [ ] Custom domain is configured (if applicable)
- [ ] SSL is working (should be automatic with Heroku)

## File Structure Summary

Your application includes these Heroku-ready files:
- `Procfile` - Tells Heroku how to run your app
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `portfolio_blog/settings/production.py` - Production-ready Django settings
- `HEROKU_ENV_VARS.md` - Environment variables reference

Your Django application is now ready for production deployment on Heroku! 🚀