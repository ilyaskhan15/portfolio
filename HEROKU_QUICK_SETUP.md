# Heroku Deployment - Quick Setup Instructions

Your Heroku app has been created: **ilyaskhan15-portfolio**
URL: https://ilyaskhan15-portfolio-06167da62ba7.herokuapp.com/

## Status: ✅ Partially Complete

### ✅ What's Already Done:
- Heroku app created: `ilyaskhan15-portfolio`
- PostgreSQL database added
- Essential environment variables set:
  - `DJANGO_SETTINGS_MODULE`
  - `SECRET_KEY`
  - `DEBUG=False`
  - `ALLOWED_HOSTS`
  - `CSRF_TRUSTED_ORIGINS`

### 🔧 What You Need to Do Next:

#### 1. Set Up Cloudinary (Required for media files)
1. Sign up at https://cloudinary.com (if you haven't already)
2. Get your credentials from the dashboard
3. Run these commands with your actual values:

```bash
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name -a ilyaskhan15-portfolio
heroku config:set CLOUDINARY_API_KEY=your-api-key -a ilyaskhan15-portfolio
heroku config:set CLOUDINARY_API_SECRET=your-api-secret -a ilyaskhan15-portfolio
```

#### 2. Deploy Your Application
```bash
# Add and commit any changes
git add .
git commit -m "Ready for Heroku deployment"

# Push to Heroku
git push heroku main
```

#### 3. Run Initial Setup
```bash
# Migrations will run automatically via Procfile, but you can run manually if needed:
heroku run python manage.py migrate -a ilyaskhan15-portfolio

# Create a superuser account
heroku run python manage.py createsuperuser -a ilyaskhan15-portfolio
```

#### 4. Open Your App
```bash
heroku open -a ilyaskhan15-portfolio
```

### 📝 Optional: Email Configuration
If you want contact forms to work, set up email:
```bash
heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend -a ilyaskhan15-portfolio
heroku config:set EMAIL_HOST=smtp.gmail.com -a ilyaskhan15-portfolio
heroku config:set EMAIL_PORT=587 -a ilyaskhan15-portfolio
heroku config:set EMAIL_USE_TLS=True -a ilyaskhan15-portfolio
heroku config:set EMAIL_HOST_USER=your-email@gmail.com -a ilyaskhan15-portfolio
heroku config:set EMAIL_HOST_PASSWORD=your-app-password -a ilyaskhan15-portfolio
```

### 🔍 Troubleshooting Commands
```bash
# View logs
heroku logs --tail -a ilyaskhan15-portfolio

# Check configuration
heroku config -a ilyaskhan15-portfolio

# Check addons
heroku addons -a ilyaskhan15-portfolio

# Restart app
heroku restart -a ilyaskhan15-portfolio
```

### 🚀 Next Steps Summary:
1. Set up Cloudinary credentials
2. Run `git push heroku main`
3. Create superuser with `heroku run python manage.py createsuperuser -a ilyaskhan15-portfolio`
4. Visit your live app at: https://ilyaskhan15-portfolio-06167da62ba7.herokuapp.com/

Your Django portfolio blog is ready to go live! 🎉