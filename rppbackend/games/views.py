from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status
from rest_framework.response import Response    
from .models import Game, GameInvitation
from .serializers import GameListSerializer, GameInvitationListSerializer, GameInvitationPostSerializer
from django.contrib.auth.models import User 
from datetime import datetime
from profiles.models import Profile

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def GameListView(request,format=None):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameListSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data 
        data['game_master'] = request.user.id 

        serializer = ProfileDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def GameDetailSlugView(request,game_slug,format=None):
    try: 
        game = Game.objects.get(slug= game_slug)
    except Game.DoesNotExist:
        return Response(data={"errors": { "profile": "Does not exist" }},status=status.HTTP_404_NOT_FOUND)

    
    if request.method == 'GET':
        serializer = GameListSerializer(game)
        return Response(serializer.data, status.HTTP_200_OK)
    
    if request.method == 'PUT':
        if game.user.id != request.user.id:
            return Response({'error': 'Permission denaied'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = request.data
        data['edited'] = datetime.now()
        data['user'] = request.user.id
        
        if 'image' in data:
            print(data['image'])
            game.image.delete()
            game.image = data['image']
            #profile.make_thumbnail(profile.image)
            game.save()
            
        
        serializer = GameListSerializer(game, data=data, partial=True)
        if serializer.is_valid():
           
            game = serializer.save()
            
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def GameGameInvitationsListView(request, game_slug, format=None):
    try: 
        game = Game.objects.get(slug= game_slug)
    except Game.DoesNotExist:
        return Response(data={"errors": { "profile": "Does not exist" }},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        game_invitations = GameInvitation.objects.filter(game=game).all()
        serializer = GameInvitationListSerializer(game_invitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        if game.game_master.id == request.user.id:
            return Response(data={"error": {"game_master": "premission_denaied"}})
        data = request.data
        if 'player_slug' in data:
            try:
                profile = Profile.objects.get(slug=data['player_slug'])
            except Profile.DoesNotExist:
                return Response(data={"error": {"player_slug": "Profile Does No Exist"}})
            data['player'] = profile.user.id

        
        data['created'] = datetime.now()
        data['edited'] = datetime.now()
        data['game'] = game.id 
        data['game_master_sender'] = request.user.id

        serializer = GameInvitationPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)



        
