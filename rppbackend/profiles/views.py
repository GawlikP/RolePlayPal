
from django.http import HttpResponse, JsonResponse

#? Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser


from rest_framework import serializers, status 

from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileDetailSerializer

from rest_framework.renderers import JSONRenderer
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from games.models import Game
from games.serializers import GameListSerializer
import json

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def ProfileListView(request, format='png'):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        if request.GET.get('username'):
            profiles = profiles.filter((Q(user__username__contains=request.GET.get('username'))) | (Q(slug__contains=request.GET.get('slug'))) )
        #if request.GET.get('slug'):
        #    profiles = profiles.filter(Q(slug__contains=request.GET.get('slug')))
        if not profiles.exists():
            return Response({"errors":{"profiles":"Nothing to show"}}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileDetailSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        data = request.data 
        data['user'] = request.user.id  
        
        img = request.FILES 

        
       
        
        profiles = Profile.objects.filter(user=request.user)
        
        if profiles:
            return Response({'errors' : {'user':'profile already exists'}}, status=status.HTTP_409_CONFLICT)
        if 'file' in img:
            data['image'] = img
        serializer = ProfileDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def ProfileDetailView(request, pk, format=None):

    try: 
        profile = Profile.objects.filter(pk= pk)
    except Profile.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    
    if request.method == 'GET':
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data, status.HTTP_200_OK)
    
    if request.method == 'PUT':
        if profile.user.id != request.user.id:
            return Response({'errors': {"user":'Permission denaied'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = request.data
        data['edited'] = datetime.now()
        data['user'] = request.user.id
        
        if 'image' in data:
            
            profile.image.delete()
            profile.image = data['image']
            profile.make_thumbnail(profile.image)
            profile.save()
            
        
        serializer = ProfileDetailSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
           
            profile = serializer.save()
            
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def ProfileDetailSlugView(request, profile_slug, format=None):

    try: 
        profile = Profile.objects.get(slug= profile_slug)
    except Profile.DoesNotExist:
        return Response(data={"errors": { "profile": "Does not exist" }},status=status.HTTP_404_NOT_FOUND)

    
    if request.method == 'GET':
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data, status.HTTP_200_OK)
    
    if request.method == 'PUT':
        if profile.user.id != request.user.id:
            return Response({'errors': {"user":'Permission denaied'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = request.data
        data['edited'] = datetime.now()
        data['user'] = request.user.id
        
        if 'image' in data:
           
            profile.image.delete()
            profile.image = data['image']
            profile.make_thumbnail(profile.image)
            profile.save()
            
        
        serializer = ProfileDetailSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
           
            profile = serializer.save()
            
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProfileUserIdView(request, pk, format=None):
    try: 
        
       
        profile = Profile.objects.get(user__pk=pk)
    except Profile.DoesNotExist:
        return Response(data={"errors": {"profile": "Does not exist"}}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data, status.HTTP_200_OK)
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def ProfileActualUserView(request, format=None):
    id = request.user.id
    try: 
        profile = Profile.objects.get(user__id= id)
    except Profile.DoesNotExist:
        return HttpResponse(data={"errors": {"profile": "Does not exist"}},status=status.HTTP_404_NOT_FOUND)

    
    if request.method == 'GET':
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data, status.HTTP_200_OK)
    
    if request.method == 'PUT':
        if profile.user.id != id:
            return Response({'error': 'Permission denaied'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = request.data
        
        img = request.FILES

        if 'image' in data:
            #data['image'] = img
            profile.image.delete()
            profile.image = data['image']
            profile.thumbnail.delete()
            profile.save()

        data['edited'] = datetime.now()
        data['user'] = request.user.id
        serializer = ProfileDetailSerializer(profile, data=data,partial=True)
        if serializer.is_valid():
            #
            profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProfilePlayersList(request, profile_slug, format=None):
    try: 
        profile = Profile.objects.get(slug= profile_slug)
    except Profile.DoesNotExist:
        return HttpResponse(data={"errors": {"profile": "Does not exist"}},status=status.HTTP_404_NOT_FOUND)

    games = Game.objects.filter(game_master__id = profile.user.id).filter(~Q(players=None)).all()
    if not games.exists():
        return Response(data={"errors": {"games": "Do not found"}}, status=status.HTTP_404_NOT_FOUND)
    
    players = games.first().players.all()
    for g in games:
        players.union(g.players.all())

    limit = int(request.query_params.get('limit', 0))
    if limit > 1:
        profiles = Profile.objects.filter(Q(user__in=players)).all()[:limit]
    else:
        profiles = Profile.objects.filter(Q(user__in=players)).all()

    serializer = ProfileDetailSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProfileMastersList(request, profile_slug, format=None):
    try: 
        profile = Profile.objects.get(slug= profile_slug)
    except Profile.DoesNotExist:
        return HttpResponse(data={"errors": {"profile": "Does not exist"}},status=status.HTTP_404_NOT_FOUND)

    games = Game.objects.filter(players__id = profile.user.id).all()
    if not games.exists():
        return Response(data={"errors": {"games": "Do not found"}}, status=status.HTTP_404_NOT_FOUND)
    game_masters = games.values_list('game_master', flat=True)

    limit = int(request.query_params.get('limit', 0))
    if limit > 1:
        profiles = Profile.objects.filter(Q(user__in=list(game_masters))).all()[:limit]
    else:
        profiles = Profile.objects.filter(Q(user__in=list(game_masters))).all()
   

    serializer = ProfileDetailSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
