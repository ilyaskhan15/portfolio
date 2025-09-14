from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator
from taggit.models import Tag
from .models import Post, Category


class PostListView(ListView):
    """Display list of published blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_tags'] = Tag.objects.all()[:10]
        return context


class PostDetailView(DetailView):
    """Display single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')
    
    def get_object(self):
        post = super().get_object()
        # Increment view count
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related posts
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(pk=self.object.pk)[:3]
        return context


class CategoryPostsView(ListView):
    """Display posts by category"""
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category,
            status='published'
        ).select_related('category', 'author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class TagPostsView(ListView):
    """Display posts by tag"""
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            tags=self.tag,
            status='published'
        ).select_related('category', 'author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['categories'] = Category.objects.all()
        return context


class PostSearchView(ListView):
    """Search blog posts"""
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query),
                status='published'
            ).distinct().select_related('category', 'author').prefetch_related('tags')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        return context
