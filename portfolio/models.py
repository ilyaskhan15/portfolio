from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from PIL import Image
import os


class Skill(models.Model):
    """Skills for portfolio display"""
    
    SKILL_TYPES = [
        ('technical', 'Technical'),
        ('framework', 'Framework'),
        ('tool', 'Tool'),
        ('language', 'Programming Language'),
        ('soft', 'Soft Skill'),
        ('other', 'Other'),
    ]
    
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES, default='technical')
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='intermediate')
    description = models.TextField(max_length=500, blank=True)
    icon = models.ImageField(upload_to='portfolio/skills/', blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    is_featured = models.BooleanField(default=False, help_text="Display prominently on portfolio")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.icon:
            self.optimize_icon()

    def optimize_icon(self):
        """Optimize skill icon"""
        try:
            if self.icon and os.path.exists(self.icon.path):
                img = Image.open(self.icon.path)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Resize to standard icon size
                max_size = (64, 64)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(self.icon.path, 'PNG', optimize=True)
        except Exception as e:
            # Log the error but don't fail the save operation
            print(f"Error optimizing icon: {e}")
            pass


class Project(models.Model):
    """Portfolio projects"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    PROJECT_TYPES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile Application'),
        ('desktop', 'Desktop Application'),
        ('api', 'API/Backend'),
        ('data', 'Data Science/Analysis'),
        ('ml', 'Machine Learning'),
        ('game', 'Game Development'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=255, help_text="Brief one-liner description")
    description = models.TextField(help_text="Detailed project description")
    
    # Project Details
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='web')
    technologies = models.ManyToManyField(Skill, blank=True, related_name='projects')
    
    # Media
    featured_image = models.ImageField(
        upload_to='portfolio/projects/%Y/%m/',
        help_text="Main project screenshot (recommended: 1200x800px)",
        blank=True,
        null=True
    )
    featured_image_alt = models.CharField(max_length=255, blank=True)
    
    # Additional Images (for project gallery)
    image_1 = models.ImageField(upload_to='portfolio/projects/%Y/%m/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='portfolio/projects/%Y/%m/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='portfolio/projects/%Y/%m/', blank=True, null=True)
    
    # Links
    live_url = models.URLField(blank=True, help_text="Live project URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    demo_url = models.URLField(blank=True, help_text="Demo/Preview URL")
    
    # Project Status and Dates
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank for ongoing projects")
    
    # Portfolio Settings
    is_featured = models.BooleanField(default=False, help_text="Display prominently on portfolio")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Ensure slug is unique
        original_slug = self.slug
        counter = 1
        while Project.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
            
        if not self.meta_description:
            self.meta_description = self.short_description[:160]
            
        super().save(*args, **kwargs)
        
        # Optimize images
        for image_field in ['featured_image', 'image_1', 'image_2', 'image_3']:
            image = getattr(self, image_field)
            if image:
                self.optimize_project_image(image)

    def optimize_project_image(self, image_field):
        """Optimize project images"""
        try:
            if image_field and os.path.exists(image_field.path):
                img = Image.open(image_field.path)
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large
                max_size = (1200, 800)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(image_field.path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            # Log the error but don't fail the save operation
            print(f"Error optimizing image: {e}")
            pass

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    @property
    def is_ongoing(self):
        return self.end_date is None

    @property
    def duration(self):
        if self.start_date:
            end = self.end_date or timezone.now().date()
            delta = end - self.start_date
            if delta.days < 30:
                return f"{delta.days} days"
            elif delta.days < 365:
                months = delta.days // 30
                return f"{months} month{'s' if months > 1 else ''}"
            else:
                years = delta.days // 365
                return f"{years} year{'s' if years > 1 else ''}"
        return "Duration not specified"


class Education(models.Model):
    """Education background"""
    
    DEGREE_TYPES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('bootcamp', 'Bootcamp'),
        ('course', 'Online Course'),
        ('other', 'Other'),
    ]
    
    institution = models.CharField(max_length=200)
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPES)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True, help_text="GPA, Grade, or similar")
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.get_degree_type_display()} in {self.field_of_study} - {self.institution}"


class Experience(models.Model):
    """Work experience"""
    
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('volunteer', 'Volunteer'),
    ]
    
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    skills_used = models.ManyToManyField(Skill, blank=True, related_name='experiences')
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.position} at {self.company}"


class Profile(models.Model):
    """Personal profile information"""
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, help_text="Professional title or tagline")
    bio = models.TextField(help_text="Brief professional bio")
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Media
    profile_image = models.ImageField(upload_to='portfolio/profile/', blank=True, null=True)
    resume = models.FileField(upload_to='portfolio/resume/', blank=True, null=True)
    
    # Social Links
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    # SEO and Meta
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            self.optimize_profile_image()

    def optimize_profile_image(self):
        """Optimize profile image"""
        try:
            if self.profile_image and os.path.exists(self.profile_image.path):
                img = Image.open(self.profile_image.path)
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Make square and resize
                size = min(img.size)
                img = img.crop(((img.width - size) // 2, (img.height - size) // 2, 
                               (img.width + size) // 2, (img.height + size) // 2))
                
                max_size = (400, 400)
                if img.size[0] > max_size[0]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(self.profile_image.path, 'JPEG', quality=90, optimize=True)
        except Exception as e:
            # Log the error but don't fail the save operation
            print(f"Error optimizing profile image: {e}")
            pass
