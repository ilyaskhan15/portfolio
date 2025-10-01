from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import os
import mimetypes
from .models import Project, Skill, Experience, Education, Profile

User = get_user_model()


class HomeView(TemplateView):
    """Dynamic homepage with latest content"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get profile
        try:
            context['profile'] = Profile.objects.filter(is_active=True).first()
        except Profile.DoesNotExist:
            context['profile'] = None
        
        # Get latest project
        context['latest_project'] = Project.objects.filter(
            status='published'
        ).order_by('-created_at').first()
        
        # Get latest football article (from blog app)
        from blog.models import Post
        context['latest_football_post'] = Post.objects.filter(
            status='published',
            category__name__iexact='football'
        ).order_by('-published_at').first()
        
        # Get latest 2 technical articles
        context['latest_tech_posts'] = Post.objects.filter(
            status='published'
        ).exclude(
            category__name__iexact='football'
        ).order_by('-published_at')[:2]
        
        # Get featured skills (for skills section)
        context['featured_skills'] = Skill.objects.filter(
            is_featured=True
        ).order_by('order')[:6]
        
        return context


@csrf_exempt
def create_users(request):
    """Emergency user creation endpoint for production"""
    
    # Only allow in production or debug mode
    if not settings.DEBUG and 'onrender.com' not in request.get_host():
        return HttpResponse("Not allowed", status=403)
    
    results = []
    
    try:
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            results.append("✅ Admin user created successfully")
        else:
            # Update password in case it was wrong
            admin_user.set_password('admin123')
            admin_user.save()
            results.append("✅ Admin user already exists (password updated)")
        
        # Create ilyas user
        ilyas_user, created = User.objects.get_or_create(
            username='ilyas',
            defaults={
                'email': 'ilyaskhanqwer0088@gmail.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            ilyas_user.set_password('Kkhan123')
            ilyas_user.save()
            results.append("✅ Ilyas user created successfully")
        else:
            # Update password in case it was wrong
            ilyas_user.set_password('Kkhan123')
            ilyas_user.save()
            results.append("✅ Ilyas user already exists (password updated)")
        
        # Show all superusers
        superusers = User.objects.filter(is_superuser=True)
        results.append(f"📊 Total superusers: {superusers.count()}")
        for user in superusers:
            results.append(f"   - {user.username} ({user.email})")
        
        results.append("\n🔑 Login credentials:")
        results.append("   admin / admin123")
        results.append("   ilyas / Kkhan123")
        results.append("\n🌐 Admin URL: /admin/")
        
    except Exception as e:
        results.append(f"❌ Error: {str(e)}")
    
    return HttpResponse("\n".join(results), content_type="text/plain")


class PortfolioView(TemplateView):
    """Main portfolio page"""
    template_name = 'portfolio/portfolio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.filter(is_active=True).first()
        except Profile.DoesNotExist:
            context['profile'] = None
            
        context['featured_projects'] = Project.objects.filter(
            is_featured=True, 
            status='published'
        ).order_by('order')[:6]
        
        context['featured_skills'] = Skill.objects.filter(
            is_featured=True
        ).order_by('order')[:8]
        
        context['recent_experiences'] = Experience.objects.filter(
            is_current=True
        ).order_by('order')[:3]
        
        return context


class ProjectDetailView(DetailView):
    """Individual project detail page"""
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(status='published').prefetch_related('technologies')


class SkillsView(ListView):
    """Skills showcase page"""
    model = Skill
    template_name = 'portfolio/skills.html'
    context_object_name = 'skills'
    
    def get_queryset(self):
        return Skill.objects.all().order_by('skill_type', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group skills by type
        skills_by_type = {}
        for skill in context['skills']:
            skill_type = skill.get_skill_type_display()
            if skill_type not in skills_by_type:
                skills_by_type[skill_type] = []
            skills_by_type[skill_type].append(skill)
        
        context['skills_by_type'] = skills_by_type
        return context


class ExperienceView(TemplateView):
    """Experience and education page"""
    template_name = 'portfolio/experience.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all().order_by('order')
        context['education'] = Education.objects.all().order_by('order')
        return context


class ResumeDownloadView(TemplateView):
    """Handle resume/CV download"""
    template_name = 'portfolio/resume_not_found.html'
    
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.filter(is_active=True).first()
            if profile and profile.resume:
                # Check if file is stored on Cloudinary
                if hasattr(profile.resume, 'url') and 'cloudinary' in profile.resume.url:
                    # For Cloudinary files, redirect to the direct URL
                    from django.shortcuts import redirect
                    return redirect(profile.resume.url)
                
                # For local files
                if hasattr(profile.resume, 'path') and os.path.exists(profile.resume.path):
                    file_path = profile.resume.path
                    
                    # Determine content type
                    content_type, _ = mimetypes.guess_type(file_path)
                    if not content_type:
                        content_type = 'application/octet-stream'
                    
                    # Get file extension
                    file_ext = os.path.splitext(file_path)[1]
                    filename = f"{profile.full_name}_Resume{file_ext}"
                    
                    # Open and return file
                    file_handle = open(file_path, 'rb')
                    response = FileResponse(file_handle, content_type=content_type)
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    response['Content-Length'] = os.path.getsize(file_path)
                    return response
        except Exception as e:
            # Log the error for debugging
            print(f"Resume download error: {e}")
            import traceback
            traceback.print_exc()
        
        # If no resume is found, render a template instead of raising 404
        return self.render_to_response(self.get_context_data())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        return context
