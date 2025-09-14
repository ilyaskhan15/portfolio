from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Project, Skill, Experience, Education, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'email', 'is_active', 'profile_image_preview']
    list_filter = ['is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'title', 'email']
    readonly_fields = ['created_at', 'updated_at', 'profile_image_preview_large']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Media', {
            'fields': ('profile_image', 'profile_image_preview_large', 'resume')
        }),
        ('Social Links', {
            'fields': ('website', 'linkedin', 'github', 'twitter', 'instagram'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.profile_image.url
            )
        return 'No image'
    profile_image_preview.short_description = 'Image'
    
    def profile_image_preview_large(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: cover; border-radius: 50%;" />',
                obj.profile_image.url
            )
        return 'No profile image uploaded'
    profile_image_preview_large.short_description = 'Profile Image Preview'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'skill_type', 'proficiency', 'years_experience', 
        'is_featured', 'order', 'icon_preview'
    ]
    list_filter = ['skill_type', 'proficiency', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_featured']
    readonly_fields = ['created_at', 'icon_preview_large']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'skill_type', 'proficiency', 'description')
        }),
        ('Experience', {
            'fields': ('years_experience',)
        }),
        ('Media', {
            'fields': ('icon', 'icon_preview_large')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 30px; height: 30px; object-fit: cover;" />',
                obj.icon.url
            )
        return 'No icon'
    icon_preview.short_description = 'Icon'
    
    def icon_preview_large(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 64px; height: 64px; object-fit: cover;" />',
                obj.icon.url
            )
        return 'No icon uploaded'
    icon_preview_large.short_description = 'Icon Preview'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'project_type', 'status', 'is_featured', 
        'order', 'duration_display', 'featured_image_preview'
    ]
    list_filter = ['project_type', 'status', 'is_featured', 'start_date']
    search_fields = ['title', 'short_description', 'description']
    list_editable = ['order', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 'updated_at', 'duration_display', 
        'featured_image_preview_large', 'is_ongoing_display'
    ]
    filter_horizontal = ['technologies']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Project Details', {
            'fields': ('project_type', 'technologies', 'status')
        }),
        ('Media', {
            'fields': (
                'featured_image', 'featured_image_alt', 'featured_image_preview_large',
                'image_1', 'image_2', 'image_3'
            ),
            'classes': ('collapse',)
        }),
        ('Links', {
            'fields': ('live_url', 'github_url', 'demo_url')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration_display', 'is_ongoing_display')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('technologies')
    
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
    
    def duration_display(self, obj):
        return obj.duration
    duration_display.short_description = 'Duration'
    
    def is_ongoing_display(self, obj):
        return 'Yes' if obj.is_ongoing else 'No'
    is_ongoing_display.short_description = 'Ongoing Project'
    is_ongoing_display.boolean = True
    
    actions = ['make_published', 'make_draft', 'mark_featured', 'unmark_featured']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} projects marked as published.')
    make_published.short_description = 'Mark selected projects as published'
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} projects marked as draft.')
    make_draft.short_description = 'Mark selected projects as draft'
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} projects marked as featured.')
    mark_featured.short_description = 'Mark selected projects as featured'
    
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} projects unmarked as featured.')
    unmark_featured.short_description = 'Unmark selected projects as featured'


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [
        'position', 'company', 'employment_type', 'is_current', 
        'start_date', 'end_date', 'order'
    ]
    list_filter = ['employment_type', 'is_current', 'start_date']
    search_fields = ['position', 'company', 'description']
    list_editable = ['order', 'is_current']
    readonly_fields = ['duration_display']
    filter_horizontal = ['skills_used']
    
    fieldsets = (
        ('Position Details', {
            'fields': ('position', 'company', 'employment_type', 'location')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current', 'duration_display')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Skills', {
            'fields': ('skills_used',)
        }),
        ('Display Settings', {
            'fields': ('order',)
        })
    )
    
    def duration_display(self, obj):
        if obj.start_date:
            end = obj.end_date or timezone.now().date()
            delta = end - obj.start_date
            if delta.days < 30:
                return f"{delta.days} days"
            elif delta.days < 365:
                months = delta.days // 30
                return f"{months} month{'s' if months > 1 else ''}"
            else:
                years = delta.days // 365
                return f"{years} year{'s' if years > 1 else ''}"
        return "Duration not specified"
    duration_display.short_description = 'Duration'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = [
        'institution', 'degree_type', 'field_of_study', 
        'is_current', 'start_date', 'end_date', 'order'
    ]
    list_filter = ['degree_type', 'is_current', 'start_date']
    search_fields = ['institution', 'field_of_study', 'description']
    list_editable = ['order', 'is_current']
    
    fieldsets = (
        ('Education Details', {
            'fields': ('institution', 'degree_type', 'field_of_study')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Information', {
            'fields': ('grade', 'description')
        }),
        ('Display Settings', {
            'fields': ('order',)
        })
    )
