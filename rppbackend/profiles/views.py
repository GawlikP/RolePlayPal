from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
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


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def ProfileListView(request, format='png'):
    if request.method == 'GET':
        profiles = Profile.objects.all()
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
        serializer = ProfileDetailSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)
    
    if request.method == 'PUT':
        if profile.user.id != request.user.id:
            return Response({'error': 'Permission denaied'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = JSONParser().parse(request)
        img = request.FILES

        if 'file' in img:
            data['image'] = img
        data['edited'] = datetime.now()
        data['user'] = request.user.id
        serializer = ProfileDetailSerializer(profile, data=data)
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
            return Response({'error': 'Permission denaied'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = request.data
        data['edited'] = datetime.now()
        data['user'] = request.user.id
        
        if 'image' in data:
            print(data['image'])
            profile.image = data['image']
            profile.save()
            
        
        serializer = ProfileDetailSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
           
            profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)