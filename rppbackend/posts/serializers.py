from rest_framework import serializers 
from .models import Post 
from post_category.models import PostCategory
from private_messages.serializers import MessageUserSerializer

class CategoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name','slug']


class PostPostSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta: 
        model = Post 
        fields = ['id', 'category', 'category_name', 'created', 'deleted', 'title', 'content', 'pluses', 'minuses', 'author', 'author_username', 'shadowed', 'reports', 'slug', 'get_absolute_url', 'get_image', 'get_thumbnail']

class PostDetailSerializer(serializers.ModelSerializer):
    category = CategoriesListSerializer(read_only=True)
    author = MessageUserSerializer(read_only=True)
    class Meta: 
        model = Post 
        fields = ['id', 'category', 'created', 'deleted', 'title', 'content', 'pluses', 'minuses', 'author', 'shadowed', 'reports', 'slug', 'get_absolute_url', 'get_image', 'get_thumbnail']


class PostListSerializer(serializers.ModelSerializer):

    category_name = serializers.ReadOnlyField(source='category.name')
    
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta: 
        model = Post 
        read_only_fields = ('id', 'author', 'slug')
        fields = ['id', 'category', 'category_name', 'created', 'deleted', 'title', 'content', 'pluses', 'minuses', 'author', 'author_username', 'shadowed', 'reports', 'slug', 'get_absolute_url', 'get_image', 'get_thumbnail']
        
