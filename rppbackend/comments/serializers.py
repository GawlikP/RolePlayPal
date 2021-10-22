from rest_framework import serializers
from .models import PostComment
from django.contrib.auth.models import User 
from posts.models import Post

class PostCommentListSerialzier(serializers.ModelSerializer):

    user_username = serializers.ReadOnlyField(source='user.username')
    post_absolute_url = serializers.ReadOnlyField(source='post.get_absolute_url')


    class Meta:
        model = PostComment
        #read_only_fields = ('id', 'created')
        fields = ['id', 'created', 'content', 'user', 'user_username', 'post', 'post_absolute_url']