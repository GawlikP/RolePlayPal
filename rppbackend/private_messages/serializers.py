from rest_framework import serializers
from .models import PrivateMessage, MessageCredential
from django.contrib.auth.models import User 
from games.serializers import PlayerSerializer



class PrivateMessageListSerializer(serializers.ModelSerializer):

    receiver_user = PlayerSerializer(read_only=True)
    sender_user = PlayerSerializer(read_only=True)

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
    
    user_from = PlayerSerializer(read_only=True)
    user_to = PlayerSerializer(read_only=True)

    class Meta:
        model = MessageCredential
        read_only_field = ('id', 'created')
        fields = ['id', 'created', 'user_from', 'user_to', 'status']

class MessageCredentialPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageCredential
        read_only_field = ('id', 'created')
        fields = ['id', 'created', 'user_from', 'user_to', 'status']
        