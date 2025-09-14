from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'posts_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def posts_count(self, obj):
        count = obj.posts.filter(status='published').count()
        if count > 0:
            url = reverse('admin:blog_post_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'
    posts_count.short_description = 'Published Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'author', 'status', 'views_count', 
        'reading_time', 'featured_image_preview', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'created_at', 'updated_at', 'tags'
    ]
    search_fields = ['title', 'excerpt', 'content', 'meta_keywords']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 'updated_at', 'views_count', 'reading_time_display',
        'featured_image_preview_large'
    ]
    # Remove filter_horizontal for tags since TaggableManager doesn't support it
    # Tags will be managed through the widget provided by django-taggit
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'status')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_image_alt', 'featured_image_preview_large'),
            'classes': ('collapse',)
        }),
        ('Organization', {
            'fields': ('author', 'category', 'tags')
        }),
        ('SEO & Meta', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('published_at',)
        }),
        ('Analytics', {
            'fields': ('views_count', 'reading_time_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author').prefetch_related('tags')
    
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return 'No image'
    featured_image_preview.short_description = 'Image'
    
    def featured_image_preview_large(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 8px;" />',
                obj.featured_image.url
            )
        return 'No featured image uploaded'
    featured_image_preview_large.short_description = 'Featured Image Preview'
    
    def reading_time_display(self, obj):
        time = obj.get_reading_time()
        return f"{time} minute{'s' if time != 1 else ''}"
    reading_time_display.short_description = 'Estimated Reading Time'
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        
        # Auto-calculate reading time
        obj.reading_time = obj.get_reading_time()
        
        super().save_model(request, obj, form, change)
    
    actions = ['make_published', 'make_draft', 'make_archived']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts marked as published.')
    make_published.short_description = 'Mark selected posts as published'
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts marked as draft.')
    make_draft.short_description = 'Mark selected posts as draft'
    
    def make_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} posts marked as archived.')
    make_archived.short_description = 'Mark selected posts as archived'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'is_approved', 'created_at', 'comment_preview']
    list_filter = ['is_approved', 'created_at', 'post']
    search_fields = ['author_name', 'author_email', 'content']
    readonly_fields = ['created_at']
    raw_id_fields = ['post', 'parent']
    
    fieldsets = (
        ('Comment Details', {
            'fields': ('post', 'author_name', 'author_email', 'content')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'parent')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def comment_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    comment_preview.short_description = 'Comment Preview'
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments unapproved.')
    unapprove_comments.short_description = 'Unapprove selected comments'
