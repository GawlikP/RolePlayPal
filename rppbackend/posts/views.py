from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#? Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser

from .serializers import PostDetailSerializer, PostListSerializer, CategoriesListSerializer
from .models import Post
from rest_framework import status 

from rest_framework.response import Response

from post_category.models import PostCategory

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def PostListView(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True) 

        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data 
        print(request.user.id)
        data['author'] = request.user.id
        serializer = PostDetailSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def PostDetailView(request, category_slug, post_slug, format=None):

    try:
        post = Post.objects.filter(category__slug=category_slug).get(slug=post_slug)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostDetailSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.erorrs, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CategoriesListView(request, format=None):
    if request.method == 'GET':
        categories = PostCategory.objects.all()
        serializer = CategoriesListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)