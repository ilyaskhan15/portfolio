from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Portfolio main pages
    path('', views.PortfolioView.as_view(), name='portfolio'),
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Skills and experience
    path('skills/', views.SkillsView.as_view(), name='skills'),
    path('experience/', views.ExperienceView.as_view(), name='experience'),
    
    # CV/Resume download
    path('resume/', views.ResumeDownloadView.as_view(), name='resume_download'),
    
    # Emergency user creation (for production setup)
    path('create-users/', views.create_users, name='create_users'),
]