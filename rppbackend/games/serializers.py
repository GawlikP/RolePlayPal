from rest_framework import serializers
from .models import Game, GameInvitation

from django.contrib.auth.models import User
from profiles.serializers import ProfileDetailSerializer
from profiles.models import Profile


class PlayerSerializer(serializers.ModelSerializer):
    
    profile_slug = serializers.SerializerMethodField()
    profile_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = User 
        read_only_fields = ('id','username','email')
        fields = ['id','username','email', 'profile_slug','profile_thumbnail']
    
    def get_profile_slug(self,obj):
        try:
            profile = Profile.objects.get(user__id =obj.id)
            return profile.slug 
        except Profile.DoesNotExist:
            return ''
    def get_profile_thumbnail(self,obj):
        try:
            profile = Profile.objects.get(user__id=obj.id)
            return profile.get_thumbnail()
        except Profile.DoesNotExist:
            return ''


class GameDetailSerializer(serializers.ModelSerializer):
    pass 

class GameListSerializer(serializers.ModelSerializer):

    players = PlayerSerializer(read_only= True, many = True)
    game_master = PlayerSerializer(read_only=False)

    class Meta:
        model = Game 
        read_only_fields = ('id','slug', 'room_key')
        fields = ['id','slug','created','edited','deleted','game_master', 'edited','next_game','description','name','players','room_key','get_image']
 
class GamePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        read_only_fields = ('id','slug')
        fields = ['id','slug','created','game_master', 'edited','next_game','description','name','players','room_key','get_image']

class GameInvitationListSerializer(serializers.ModelSerializer):

    game_master_sender = PlayerSerializer(read_only=True)
    player = PlayerSerializer(read_only=True)
    game_slug = serializers.ReadOnlyField(source='game.slug')
    game_name = serializers.ReadOnlyField(source='game.name')
    game = GameListSerializer(read_only=True)

    class Meta:
        model = GameInvitation
        fields = ['id','created','edited','game_master_sender','game','game_slug','game_name','player','text','readed','accepted', 'canceled','hide']


class GameInvitationPostSerializer(serializers.ModelSerializer):

    game_master_sender_username = serializers.ReadOnlyField(source='game_master_sender.username')
    game_master_sender_slug = serializers.SerializerMethodField()
    game_slug = serializers.ReadOnlyField(source='game.slug')
    player_slug = serializers.SerializerMethodField()

    class Meta:
        model = GameInvitation
        read_only_fields = ['id','game_master_username','game_slug ', 'get_absolute_url']
        fields = ['id','created','edited','game_master_sender','game_master_sender_username','game_master_sender_slug','game','game_slug','player','player_slug','text','readed','accepted', 'canceled','hide','get_absolute_url']
    
    def get_game_master_sender_slug(self,obj):
        try:
            profile = Profile.objects.get(user__id =obj.game_master_sender.id)
            return profile.slug 
        except Profile.DoesNotExist:
            return ''
    def get_player_slug(self,obj):
        try:
            profile = Profile.objects.get(user__id =obj.player.id)
            return profile.slug 
        except Profile.DoesNotExist:
            return ''