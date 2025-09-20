from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
import os


class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    """Blog post model with SEO and rich content features"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Brief description for SEO and previews")
    
    # Content
    content = RichTextUploadingField()
    
    # Media
    featured_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Main image for the post (recommended: 1200x630px)"
    )
    featured_image_alt = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alt text for accessibility and SEO"
    )
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = TaggableManager(blank=True, help_text="Add relevant tags separated by commas")
    
    # Status and Publishing
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # SEO Fields
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Meta description for SEO (max 160 characters)"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="SEO keywords separated by commas"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Analytics
    views_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(
        default=0,
        help_text="Estimated reading time in minutes"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category', '-published_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Ensure slug is unique
        original_slug = self.slug
        counter = 1
        while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
            
        # Auto-generate meta description from excerpt if not provided
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
            
        super().save(*args, **kwargs)
        
        # Optimize image if uploaded
        if self.featured_image:
            self.optimize_image()

    def optimize_image(self):
        """Optimize featured image for web"""
        try:
            if self.featured_image and os.path.exists(self.featured_image.path):
                img = Image.open(self.featured_image.path)
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large
                max_size = (1200, 630)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(self.featured_image.path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            # Log the error but don't fail the save operation
            print(f"Error optimizing blog image: {e}")
            pass

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_reading_time(self):
        """Calculate estimated reading time"""
        if self.content:
            word_count = len(self.content.split())
            reading_time = max(1, word_count // 200)  # Average 200 words per minute
            return reading_time
        return 0

    @property
    def is_published(self):
        return self.status == 'published'


class Comment(models.Model):
    """Blog post comments (for future implementation)"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author_name} on {self.post.title}'
