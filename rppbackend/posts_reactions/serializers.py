from rest_framework import serializers 
from .models import Post 
from django.contrib.auth.models import User
from .models import PostReaction


class ReactionListSerializer(serializers.ModelSerializer):

    user_username = serializers.ReadOnlyField(source='user.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    post_absolute_url = serializers.ReadOnlyField(source='post.get_absolute_url')

    class Meta:
        model = PostReaction
        read_only_fields = ('id','created')
        fields = ['id', 'created', 'user', 'user_username','post', 'post_title', 'post_absolute_url', 'state']
