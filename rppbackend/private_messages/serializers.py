from rest_framework import serializers
from .models import PrivateMessage, MessageCredential
from django.contrib.auth.models import User 
from games.serializers import PlayerSerializer
from profiles.serializers import ProfileDetailSerializer, PlaneProfileSerializer
from profiles.models import Profile

class MessageUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        read_only_field = ('id', 'username', 'profile')
        fields = ['id', 'username', 'profile']
    def get_profile(self, obj):
        try:
            profile = Profile.objects.get(user__id=obj.id)
            serializer = PlaneProfileSerializer(profile)
            return serializer.data
        except Profile.DoesNotExist:
            return ''

class PrivateMessageListSerializer(serializers.ModelSerializer):

    receiver_user = MessageUserSerializer(read_only=True)
    sender_user = MessageUserSerializer(read_only=True)

    class Meta:
        model = PrivateMessage
        read_only_field = ('id', 'created', 'sended')
        fields = ['id', 'created', 'sended', 'text', 'receiver_user', 'sender_user', 'readed']

class PrivateMessagePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivateMessage
        read_only_field = ('id',)
        fields = ['id', 'created', 'sended', 'text', 'receiver_user', 'sender_user', 'readed']

class MessageCredentialListSerializer(serializers.ModelSerializer):
    
    user_from = MessageUserSerializer(read_only=True)
    user_to = MessageUserSerializer(read_only=True)

    class Meta:
        model = MessageCredential
        read_only_field = ('id', 'created')
        fields = ['id', 'created', 'user_from', 'user_to', 'status']

class MessageCredentialPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageCredential
        read_only_field = ('id', 'created')
        fields = ['id', 'created', 'user_from', 'user_to', 'status']
        