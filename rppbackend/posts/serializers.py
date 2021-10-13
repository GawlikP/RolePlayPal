from rest_framework import serializers 
from .models import Post 
from post_category.models import PostCategory


class PostDetailSerializer(serializers.ModelSerializer):
    
    category_name = serializers.ReadOnlyField(source='category.name')
    
    author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta: 
        model = Post 
        fields = ['id', 'category', 'category_name', 'created', 'deleted', 'title', 'content', 'pluses', 'minuses', 'author', 'author_username', 'shadowed', 'reports', 'slug', 'get_absolute_url', 'get_image', 'get_thumbnail']

class PostListSerializer(serializers.ModelSerializer):

    category_name = serializers.ReadOnlyField(source='category.name')
    
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta: 
        model = Post 
        read_only_fields = ('id', 'author')
        fields = ['id', 'category', 'category_name', 'created', 'deleted', 'title', 'content', 'pluses', 'minuses', 'author', 'author_username', 'shadowed', 'reports', 'slug', 'get_absolute_url', 'get_image', 'get_thumbnail']
        
class CategoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name','slug']
