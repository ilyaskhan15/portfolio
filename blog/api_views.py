from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer


class PostViewSet(viewsets.ModelViewSet):
    """API viewset for blog posts"""
    queryset = Post.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tags']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'views_count']
    ordering = ['-created_at']
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for blog categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'