# Render.com Deployment Guide

This guide provides step-by-step instructions for deploying your Django Portfolio Blog to Render.com.

## Prerequisites

1. **Render.com Account**: Sign up at [render.com](https://render.com)
2. **GitHub Account**: Required for repository hosting
3. **Git**: Installed on your local machine
4. **GitHub Repository**: Your code should be in a GitHub repository
5. **Database Requirements**: PostgreSQL database (can be created on Render.com)

## Deployment Steps

### Step 0: Git and GitHub Setup (First Time Only)

If you haven't already set up Git and GitHub for this project, follow these steps:

#### A. Initialize Git Repository

1. **Navigate to your project directory:**
   ```bash
   cd /home/ik/Desktop/BlogPost
   ```

2. **Initialize Git repository:**
   ```bash
   git init
   ```

3. **Add all files to Git:**
   ```bash
   git add .
   ```

4. **Create initial commit:**
   ```bash
   git commit -m "Initial commit: Django Portfolio Blog project"
   ```

#### B. Create GitHub Repository

1. **Go to GitHub.com** and log in to your account
2. **Create a new repository:**
   - Click the "+" icon in the top right corner
   - Select "New repository"
   - **Repository name**: `django-portfolio-blog` (or your preferred name)
   - **Description**: "Django-based portfolio and blog website"
   - **Visibility**: Public or Private (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click "Create repository"

#### C. Connect Local Repository to GitHub

1. **Add GitHub remote:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/django-portfolio-blog.git
   ```
   Replace `YOUR_USERNAME` with your actual GitHub username.

2. **Push to GitHub:**
   ```bash
   git branch -M main
   git push -u origin main
   ```

#### D. Verify Upload

1. **Refresh your GitHub repository page**
2. **Confirm all files are uploaded** (you should see your Django project files)
3. **Check that sensitive files are ignored** (verify `.env` files are NOT visible)

### Step 1: Create PostgreSQL Database

1. **Log into Render.com Dashboard**
2. **Create New PostgreSQL Database:**
   - Click "New" → "PostgreSQL"
   - **Name**: `portfolio-blog-database` (or your preferred name)
   - **Database**: `portfolio` (or your preferred database name)
   - **User**: Will be auto-generated
   - **Region**: Choose closest to your target audience
   - **PostgreSQL Version**: Latest stable version
   - **Plan**: Free tier or your preferred plan

3. **Save Database Information:**
   - Copy the **External Database URL** (starts with `postgresql://`)
   - This will be used in your web service environment variables

### Step 2: Prepare Your Repository

Ensure your GitHub repository contains these files (already included in this project):

- `render.yaml` - Render service configuration
- `build.sh` - Build script for deployment
- `runtime.txt` - Python version specification
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies
- Modular settings in `portfolio_blog/settings/`

### Step 3: Create Web Service

1. **Create New Web Service:**
   - Click "New" → "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Connect your GitHub account if not already connected

2. **Select Repository:**
   - Choose the repository containing your Django project
   - Click "Connect"

3. **Configure Service Settings:**
   - **Name**: `your-portfolio-blog` (choose a unique name)
   - **Environment**: Python 3
   - **Region**: Same as your database region
   - **Branch**: `main` (or your deployment branch)
   - **Root Directory**: Leave blank (unless your Django project is in a subdirectory)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn portfolio_blog.wsgi:application`

### Step 4: Configure Environment Variables

In your web service settings, go to the "Environment" tab and add these variables:

#### Required Variables

```env
# Database Connection
DATABASE_URL=postgresql://username:password@hostname:port/database_name
# Use the External Database URL from Step 1

# Django Configuration
SECRET_KEY=your-super-secret-key-minimum-50-characters-long
DEBUG=False
DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production

# Allowed Hosts
ALLOWED_HOSTS=your-app-name.onrender.com
# Replace 'your-app-name' with your actual Render service name
```

#### Optional Variables (for enhanced functionality)

```env
# Email Configuration (for contact forms, password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Security Headers (recommended for production)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### Generating a Secret Key

Use this Python command to generate a secure secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy

1. **Click "Create Web Service"**
2. **Monitor the Build Process:**
   - Watch the build logs in real-time
   - The build process will:
     - Install Python dependencies
     - Run database migrations
     - Collect static files
     - Start the Gunicorn server

3. **Deployment Timeline:**
   - Initial build: 5-10 minutes
   - Subsequent deployments: 2-5 minutes

### Step 6: Post-Deployment Setup

#### Create Admin User

1. **Access Render Shell:**
   - Go to your web service dashboard
   - Click on the "Shell" tab
   - This opens a command-line interface to your deployed app

2. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   - Enter username, email, and password when prompted

#### Verify Deployment

1. **Test Your Application:**
   - Visit `https://your-app-name.onrender.com`
   - Check that the homepage loads correctly
   - Verify that static files (CSS, images) are loading

2. **Test Admin Interface:**
   - Visit `https://your-app-name.onrender.com/admin/`
   - Log in with your superuser credentials
   - Add some content to test functionality

3. **Test Database Connection:**
   - Create a blog post or portfolio item through the admin
   - Verify that data persists after page refresh

## Configuration Details

### Build Script (`build.sh`)

The build script automatically:
- Installs Python dependencies
- Runs database migrations
- Collects static files for WhiteNoise

### Settings Configuration

The project uses modular settings:
- `base.py`: Common settings
- `development.py`: Local development settings
- `production.py`: Production-specific settings

Production settings include:
- PostgreSQL database configuration
- WhiteNoise for static files
- Security headers
- Debug mode disabled
- Allowed hosts configuration

### Static Files

Static files are served by WhiteNoise, which:
- Serves static files efficiently in production
- Handles compression and caching
- Works well with Render.com's infrastructure

## Troubleshooting

### Common Issues and Solutions

#### Build Failures

**Issue**: `ModuleNotFoundError` during build
- **Solution**: Ensure all dependencies are in `requirements.txt`
- Check that dependency versions are compatible

**Issue**: Database connection error during migration
- **Solution**: Verify `DATABASE_URL` environment variable is correct
- Ensure PostgreSQL database is running and accessible

#### Runtime Issues

**Issue**: Static files not loading
- **Solution**: Check that `STATIC_ROOT` is configured in production settings
- Verify WhiteNoise is installed and configured

**Issue**: Internal Server Error (500)
- **Solution**: Check application logs in Render dashboard
- Verify all environment variables are set correctly
- Ensure `DEBUG=False` and `ALLOWED_HOSTS` includes your domain

**Issue**: Database permissions error
- **Solution**: Check PostgreSQL user permissions
- Verify database URL format and credentials

#### Performance Issues

**Issue**: Slow initial page load
- **Solution**: This is normal for free tier services (they "spin down" when idle)
- Consider upgrading to a paid plan for always-on service

### Checking Logs

1. **Build Logs**: Available during deployment process
2. **Application Logs**: Available in your service dashboard under "Logs"
3. **Database Logs**: Available in your PostgreSQL database dashboard

### Getting Help

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **Django Documentation**: [docs.djangoproject.com](https://docs.djangoproject.com)

## Best Practices

### Security

1. **Never commit sensitive data** to your repository
2. **Use strong SECRET_KEY** (minimum 50 characters)
3. **Enable security headers** in production
4. **Regularly update dependencies** for security patches

### Performance

1. **Use database indexes** for frequently queried fields
2. **Optimize images** before uploading
3. **Consider caching** for high-traffic sites
4. **Monitor application performance** using Render metrics

### Maintenance

1. **Regular backups**: Render provides automatic PostgreSQL backups
2. **Monitor logs** for errors and performance issues
3. **Keep dependencies updated** for security and performance
4. **Test deployments** in a staging environment when possible

## Cost Considerations

### Free Tier Limitations

- **Web Service**: 750 hours/month, spins down after 15 minutes of inactivity
- **PostgreSQL**: 90 days retention, 1GB storage
- **Bandwidth**: 100GB/month

### Upgrading Plans

Consider upgrading if you need:
- Always-on service (no spin-down)
- More database storage
- Higher bandwidth limits
- Custom domains with SSL
- Priority support

## Custom Domain Setup

1. **Purchase a domain** from your preferred registrar
2. **Configure DNS** to point to your Render service
3. **Add custom domain** in Render dashboard
4. **SSL certificate** will be automatically provisioned

---

Your Django Portfolio Blog is now successfully deployed on Render.com! 🎉

## Updating Your Deployment

When you make changes to your project, follow these steps to update your deployment:

### Local Development Workflow

1. **Make your changes** to the code
2. **Test locally** to ensure everything works:
   ```bash
   ./run.sh
   # Test your changes at http://127.0.0.1:8000
   ```

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Describe your changes here"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin main
   ```

5. **Automatic Deployment**: Render.com will automatically detect the changes and redeploy your application (this takes 2-5 minutes)

### Common Git Commands

```bash
# Check status of files
git status

# Add specific files
git add filename.py

# Add all modified files
git add .

# Commit with message
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes (if working with others)
git pull origin main

# View commit history
git log --oneline
```

### Managing Environment Variables

**Important**: Never commit sensitive information like:
- SECRET_KEY
- Database passwords
- API keys
- Email passwords

These should only be set in Render.com's environment variables, not in your code.

For ongoing maintenance and updates, simply push changes to your GitHub repository, and Render will automatically redeploy your application.