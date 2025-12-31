from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import os
import mimetypes
import urllib.parse
import requests
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


class AboutView(TemplateView):
    """About page for AdSense compliance"""
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        return context


class ContactView(TemplateView):
    """Contact page for AdSense compliance"""
    template_name = 'portfolio/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        return context


class PrivacyView(TemplateView):
    """Privacy Policy page for AdSense compliance"""
    template_name = 'portfolio/privacy.html'


class TermsView(TemplateView):
    """Terms of Service page for AdSense compliance"""
    template_name = 'portfolio/terms.html'


class ResumeDownloadView(TemplateView):
    """Show resume page with optional download action"""
    template_name = 'portfolio/resume_not_found.html'

    def _download_response(self, profile):
        """Return a download response for the profile resume if available."""
        if not profile or not profile.resume:
            return None

        # Cloudinary download variants
        if hasattr(profile.resume, 'url') and 'cloudinary' in profile.resume.url:
            cloudinary_url = profile.resume.url
            download_urls = []

            if '/image/upload/' in cloudinary_url:
                download_urls.append(cloudinary_url.replace('/image/upload/', '/raw/upload/fl_attachment/'))
                download_urls.append(cloudinary_url.replace('/image/upload/', '/image/upload/fl_attachment/'))

            if '/upload/' in cloudinary_url:
                parts = cloudinary_url.split('/upload/')
                if len(parts) == 2:
                    download_urls.append(f"{parts[0]}/upload/fl_attachment/{parts[1]}")

            download_urls.append(cloudinary_url)

            for attempt_url in download_urls:
                try:
                    response = requests.head(attempt_url, timeout=5)
                    if response.status_code == 200:
                        return redirect(attempt_url)
                except Exception:
                    continue

            return redirect(cloudinary_url)

        # Local file download
        if hasattr(profile.resume, 'path') and os.path.exists(profile.resume.path):
            file_path = profile.resume.path
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = 'application/octet-stream'

            file_ext = os.path.splitext(file_path)[1]
            filename = f"{profile.full_name.replace(' ', '_')}_Resume{file_ext}"

            file_handle = open(file_path, 'rb')
            response = FileResponse(file_handle, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = os.path.getsize(file_path)
            return response

        return None

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(is_active=True).first()
        download_requested = request.GET.get('download') == '1'

        if download_requested:
            try:
                download_response = self._download_response(profile)
                if download_response:
                    return download_response
            except Exception as e:
                # Log for debugging but still fall back to page render
                print(f"Resume download error: {e}")
                import traceback
                traceback.print_exc()

        return self.render_to_response(self.get_context_data(profile=profile))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = kwargs.get('profile') or Profile.objects.filter(is_active=True).first()
        context['profile'] = profile
        context['resume_available'] = bool(profile and profile.resume)
        context['resume_url'] = profile.resume.url if profile and hasattr(profile.resume, 'url') else None
        context['download_url'] = f"{reverse('portfolio:resume_download')}?download=1"
        return context
