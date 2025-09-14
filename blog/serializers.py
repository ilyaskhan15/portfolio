from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for blog categories"""
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at']
        
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for blog posts"""
    tags = TagListSerializerField()
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'featured_image_alt', 'author', 'author_name', 'category', 'category_name',
            'tags', 'status', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at', 'published_at', 'views_count', 'reading_time'
        ]
        read_only_fields = ['views_count', 'created_at', 'updated_at']
        
    def get_reading_time(self, obj):
        return obj.get_reading_time()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for blog comments"""
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'author_email', 'content', 'created_at', 'is_approved', 'parent', 'replies']
        read_only_fields = ['is_approved']
        
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        return []