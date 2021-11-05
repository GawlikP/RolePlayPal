from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#? Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser

from .serializers import PostDetailSerializer, PostListSerializer, CategoriesListSerializer
from comments.serializers import PostCommentListSerialzier
from .models import Post
from rest_framework import serializers, status 

from rest_framework.response import Response

from post_category.models import PostCategory

from posts_reactions.serializers import ReactionListSerializer
from posts_reactions.models import PostReaction

from comments.models import PostComment

from rest_framework.renderers import JSONRenderer




@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def PostListView(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True) 

        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data 
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def PostReactionsListView(request, category_slug, post_slug, format=None):
    try:
        post = Post.objects.filter(category__slug=category_slug).get(slug=post_slug)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        reactions = PostReaction.objects.filter(post = post)
        serializer = ReactionListSerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        if PostReaction.objects.filter(post=post).filter(user=request.user).exists():
            return Response({"erorr": "Reaction Already Exists"},status.HTTP_409_CONFLICT)
        data = request.data 
        data['user'] = request.user.id
        data['post'] = post.id
        serializer = ReactionListSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserPostReactionsView(request,category_slug,post_slug, format=None):
    try:
        post = Post.objects.filter(category__slug=category_slug).get(slug=post_slug)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        try:
            reactions = PostReaction.objects.filter(post= post).get(user= request.user.id)
        except PostReaction.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReactionListSerializer(reactions)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PostsReactionsListView(request, format=None):
    if request.method == 'GET':
        reactions = PostReaction.objects.all()
        serializer = ReactionListSerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserPostsReactionsView(request,format=None):
    try:
        reactions = PostReaction.objects.filter(user=request.user)
    except PostReaction.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    serializer = ReactionListSerializer(reactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','POST','PUT'])
@permission_classes([IsAuthenticated])
def PostCommentListView(request, category_slug, post_slug, format=None):    
    try:
        post = Post.objects.filter(category__slug = category_slug).get(slug= post_slug)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        try: 
            comments = PostComment.objects.filter(post = post)    
        except PostComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND) 
        serializer = PostCommentListSerialzier(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':

        data = request.data
        data['user'] = request.user.id
        data['post'] = post.id 
        serializer = PostCommentListSerialzier(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def PostCommentDetailView(request, pk, format=None):
    if request.method == 'PUT':
        data = request.data
        data['user'] = request.user.id 
        try:
            postcomment = PostComment.objects.get(pk=pk)
        except PostComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        data['post'] = postcomment.post.id
        serializer = PostCommentListSerialzier(postcomment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


