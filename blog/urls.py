from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog main pages
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Category and tag pages
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagPostsView.as_view(), name='tag_posts'),
    
    # Search
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    
    # RSS Feed (optional)
    # path('feed/', PostFeed(), name='post_feed'),
]