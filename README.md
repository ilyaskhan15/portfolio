# Portfolio Blog Django Application

A comprehensive Django-based portfolio and blog website featuring modern design, SEO optimization, and production-ready configuration.

## 🚀 Features

### Blog System
- **Rich Content Management**: CKEditor integration for rich text editing
- **SEO Optimization**: Meta tags, Open Graph, Twitter Cards
- **Categorization & Tagging**: Organize content with categories and tags
- **Search Functionality**: Full-text search across posts
- **Reading Time Estimation**: Automatic calculation of reading time
- **View Tracking**: Post popularity metrics
- **Comment System**: Ready for future comment implementation

### Portfolio Showcase
- **Project Management**: Detailed project showcases with images and tech stacks
- **Skills Tracking**: Categorized skills with proficiency levels
- **Experience Timeline**: Professional experience and education history
- **Resume Download**: PDF resume download functionality
- **Social Links Integration**: Connect all your social profiles

### Technical Features
- **REST API**: Full API for headless/mobile applications
- **Admin Interface**: Comprehensive Django admin with custom configurations
- **Image Optimization**: Automatic image resizing and compression
- **Responsive Design**: Mobile-first Tailwind CSS design
- **Performance Optimized**: Database indexing and query optimization
- **Production Ready**: Environment variables, static files, security settings

## 🛠️ Technology Stack

### Backend
- **Django 5.1.1**: Modern Python web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Production database (SQLite for development)
- **Pillow**: Image processing and optimization

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library
- **Google Fonts**: Typography (Inter font family)
- **Responsive Design**: Mobile-first approach

### Content Management
- **CKEditor**: WYSIWYG editor for rich content
- **django-taggit**: Flexible tagging system
- **Image Upload**: Automatic image optimization

### Development & Deployment
- **python-decouple**: Environment configuration
- **WhiteNoise**: Static file serving
- **Gunicorn**: WSGI server for production
- **Django Extensions**: Development utilities

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)
- Git (for version control and deployment)
- GitHub account (for deployment to Render.com)

### Quick Start

1. **Clone and Navigate**
   ```bash
   cd BlogPost
   ```

2. **Virtual Environment Setup**
   The virtual environment is already configured in the `enviroment/` directory.

3. **Install Dependencies**
   ```bash
   enviroment/bin/pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Copy and customize the `.env` file:
   ```bash
   # The .env file is already created with default values
   # Update the values as needed for your setup
   ```

5. **Database Setup**
   ```bash
   enviroment/bin/python manage.py migrate
   ```

6. **Create Admin User**
   ```bash
   enviroment/bin/python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   ./run.sh
   # Or manually: enviroment/bin/python manage.py runserver
   ```

8. **Access Your Site**
   - Website: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

### Git Setup (For Deployment)

If you plan to deploy to Render.com or any other platform, you'll need Git:

```bash
# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Django Portfolio Blog"

# Create GitHub repository and connect
git remote add origin https://github.com/YOUR_USERNAME/your-repo-name.git
git branch -M main
git push -u origin main
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## � Adding Content

### Resume Setup
1. Log into the admin panel at http://127.0.0.1:8000/admin
2. Go to **Portfolio > Profiles**
3. Create a new Profile or edit existing one
4. Upload your resume (PDF format recommended)
5. Set the profile as "Active"
6. The resume download will now work at `/portfolio/resume/`

### Content Management
- **Blog Posts**: Add articles, set categories, tags, and SEO settings
- **Portfolio Projects**: Showcase your work with images, descriptions, and technologies
- **Experience**: Add your professional experience with timeline view
- **Skills**: Display your technical skills with proficiency levels
- **Education**: Add your academic background and achievements

## �🔧 Configuration

### Environment Variables (.env)

```env
# Security
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: DATABASE_URL=postgres://username:password@localhost:5432/dbname

# Email (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Allowed Hosts (Production)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Production Deployment

#### Option 1: Manual Deployment

1. **Update Environment Variables**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=postgres://username:password@localhost:5432/portfolio_blog
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Migration**
   ```bash
   python manage.py migrate
   ```

4. **Run with Gunicorn**
   ```bash
   gunicorn portfolio_blog.wsgi:application
   ```

#### Option 2: Render.com Deployment (Recommended)

This project is pre-configured for easy deployment on Render.com with PostgreSQL database.

**Prerequisites:**
- A Render.com account
- GitHub repository with this project

**Deployment Steps:**

1. **Create PostgreSQL Database on Render.com:**
   - Go to Render Dashboard → "New" → "PostgreSQL"
   - Choose database name (e.g., `portfolio-blog-db`)
   - Select your preferred plan (Free tier available)
   - Copy the `External Database URL` provided

2. **Create Web Service on Render.com:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `your-portfolio-blog`
     - **Environment**: Python 3
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn portfolio_blog.wsgi:application`
     - **Instance Type**: Free tier or preferred plan

3. **Set Environment Variables:**
   In your Render web service, go to "Environment" and add:
   ```env
   DATABASE_URL=postgresql://username:password@hostname:port/database_name
   SECRET_KEY=your-strong-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DJANGO_SETTINGS_MODULE=portfolio_blog.settings.production
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Build process includes dependency installation and database migrations

5. **Post-Deployment Setup:**
   - Access Render Shell from your service dashboard
   - Create superuser: `python manage.py createsuperuser`
   - Your app will be live at `https://your-app-name.onrender.com`

**Render.com Configuration Files:**
- `render.yaml`: Service configuration
- `build.sh`: Build script with migrations and static files
- `runtime.txt`: Python version specification
- `.env.example`: Template for environment variables

**Production Features:**
- Automatic HTTPS and SSL certificates
- PostgreSQL database with automatic backups
- WhiteNoise for static file serving
- Gunicorn WSGI server
- Environment-based settings (development/production)
- Security headers and CSRF protection

## 📁 Project Structure

```
BlogPost/
├── enviroment/              # Virtual environment
├── portfolio_blog/          # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── blog/                   # Blog application
│   ├── models.py          # Blog models (Post, Category, Comment)
│   ├── views.py           # Blog views
│   ├── admin.py           # Admin configurations
│   ├── serializers.py     # API serializers
│   └── urls.py            # Blog URL patterns
├── portfolio/              # Portfolio application
│   ├── models.py          # Portfolio models (Project, Skill, etc.)
│   ├── views.py           # Portfolio views
│   ├── admin.py           # Admin configurations
│   ├── serializers.py     # API serializers
│   └── urls.py            # Portfolio URL patterns
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Homepage
│   ├── blog/              # Blog templates
│   └── portfolio/         # Portfolio templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files
├── staticfiles/           # Collected static files
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── run.sh                 # Development server script
└── README.md              # This file
```

## 🎨 Customization

### Adding Content

1. **Create Profile**
   - Go to Admin → Portfolio → Profiles
   - Add your personal information, photo, and social links

2. **Add Skills**
   - Go to Admin → Portfolio → Skills
   - Add your technical skills with proficiency levels

3. **Create Projects**
   - Go to Admin → Portfolio → Projects
   - Add project details, images, and technology stacks

4. **Write Blog Posts**
   - Go to Admin → Blog → Posts
   - Create categories and write articles

### Styling Customization

- **CSS**: Edit `static/css/custom.css` for custom styles
- **Templates**: Modify templates in the `templates/` directory
- **Colors**: Update Tailwind color configuration in `base.html`

### API Usage

The application provides REST APIs for all content:

- **Blog API**: `/api/posts/`, `/api/categories/`
- **Portfolio API**: `/api/portfolio/projects/`, `/api/portfolio/skills/`

Example API calls:
```bash
# Get all published posts
curl http://127.0.0.1:8000/api/posts/

# Get all projects
curl http://127.0.0.1:8000/api/portfolio/projects/

# Get specific post by slug
curl http://127.0.0.1:8000/api/posts/your-post-slug/
```

## 🚀 Performance & SEO

### Built-in Optimizations
- **Database Indexing**: Optimized queries with proper indexes
- **Image Optimization**: Automatic image resizing and compression
- **Caching**: Ready for Redis/Memcached integration
- **SEO Meta Tags**: Comprehensive meta tag implementation
- **Sitemap Ready**: Django sitemap framework integrated
- **Static File Optimization**: WhiteNoise for efficient static file serving

### SEO Features
- Meta descriptions and keywords
- Open Graph tags for social sharing
- Twitter Card integration
- Structured data ready
- Clean URL structure with slugs
- Image alt text support

## 🔒 Security Features

- Environment variable configuration
- CSRF protection
- XSS protection
- SQL injection protection
- Secure headers in production
- File upload validation
- Rate limiting ready

## 📱 Mobile Responsiveness

- Mobile-first design approach
- Touch-friendly navigation
- Optimized images for different screen sizes
- Fast loading on mobile devices

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the documentation above
2. Review the Django admin interface for content management
3. Check the console for any error messages
4. Ensure all environment variables are properly set

## 🚀 Next Steps

After setup, consider:

1. **Content Creation**: Add your profile, projects, and blog posts
2. **Customization**: Update colors, fonts, and layout to match your brand
3. **SEO Optimization**: Add your Google Analytics, Search Console
4. **Performance**: Set up caching and CDN for production
5. **Backup Strategy**: Implement database and media file backups
6. **Monitoring**: Add error tracking and performance monitoring

---

**Happy Blogging! 🎉**

Built with ❤️ using Django and Tailwind CSS