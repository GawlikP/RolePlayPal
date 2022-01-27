from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#? Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser

from .serializers import PostDetailSerializer, PostListSerializer, CategoriesListSerializer, PostPostSerializer
from comments.serializers import PostCommentListSerializer
from .models import Post
from rest_framework import serializers, status 

from rest_framework.response import Response

from post_category.models import PostCategory

from posts_reactions.serializers import ReactionListSerializer, ReactionPostSerializer
from posts_reactions.models import PostReaction

from comments.models import PostComment

from rest_framework.renderers import JSONRenderer

from django.core.paginator import Paginator

from django.contrib.auth.models import User

from django.db.models import Q

@api_view(['GET','POST']) #? Allowed methods for request
@permission_classes([IsAuthenticated]) #? Required permissions
#?  'posts/'
def PostListView(request, format=None): #* Return paged list of all Posts or Create new Post
    if request.method == 'GET': #? What needs to be done if its 'GET' request
      
        page_number = request.query_params.get('page_number', 1)    #? Get page from request params           
        page_size = request.query_params.get('page_size',5)         #? Get page size from params 
        title = request.query_params.get('title','')                #? Get title filter parameter
        category_slug = request.query_params.get('category', '')    #? Get category type filter

        posts = Post.objects.filter(deleted=False).filter(Q(title__contains=title)) #? Define if title is filtered
        if category_slug != '': #? If category filter is defined get needed data
            posts = posts.filter(category__slug=category_slug).all() 
        else:   #? If not just get all
            posts= posts.all()

        paginator = Paginator(posts, page_size)     #? Using Paginator class to easly divide models
        if int(page_number) > paginator.num_pages:  #? If page does not exists return error and done
            return Response({'error': 'Page do not exist!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostListSerializer(paginator.page(page_number), many=True) #? Serialize data
        data = {}
        data['posts'] = serializer.data #? To posts attribute parse requested posts
        data['page_numbers'] = paginator.num_pages #? Attach how many pages can be getted 
        data['next_page'] = False if int(page_number) >= paginator.num_pages else True 
        return Response(data, status=status.HTTP_200_OK) #? Finally return requested data
        
    if request.method == 'POST': #? What needs to be done if its 'POST' request
        data = request.data #? Get declared data in request body
        data['author'] = request.user.id #? Set author as Authorized user
        serializer = PostPostSerializer(data= data) #? Try to serialize data
        if serializer.is_valid(): #? If everything is ok, then create new object end return successfully
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE) #? If validation is not permitted, return list of errors

@api_view(['GET','PUT', 'DELETE'])#? Allowed methods for request
@permission_classes([IsAuthenticated])#? Required permissions
#?  'posts/<slug:category_slug>/<slug:post_slug>/'
def PostDetailView(request, category_slug, post_slug, format=None): #* Return detailed data, update data or delete data

    try:    #? Check if requested post exists
        post = Post.objects.filter(category__slug=category_slug).get(slug=post_slug) #? Try to find that post
    except Post.DoesNotExist:   #? If not, return status and error data
        return HttpResponse({'error':{'post':'Does not exits'}},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostDetailSerializer(post) #? Serialize founded post
        return Response(serializer.data, status.HTTP_200_OK) #? Return JSON of that post
    
    if request.method == 'PUT':
     
        if not request.user.id == post.author.id:   #? Check if requesting user is permitted
            return Response(data={"errors": {"author": "permission denaied"}}, status=status.HTTP_406_NOT_ACCEPTABLE) #? Permission deneied return
        data = request.data #? Fetch data from request body
        
        serializer = PostPostSerializer(post, data=data, partial=True)  #? Serialize data
        if serializer.is_valid(): #? Check if data is valid
            serializer.save()   #? save model
            return Response(serializer.data, status=status.HTTP_201_CREATED)    #? Return JSON data
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)   #? Return errors after validation

    if request.method == 'DELETE':  
        if not request.user.id == post.author.id:   #? Check if user is permitted
            return Response(data={"errors": {"author": "permission denaied"}}, status=status.HTTP_406_NOT_ACCEPTABLE) #? 

        data = {}   #? Setup data to update
        data['deleted'] = True
        data['author'] = request.user.id

        serializer = PostPostSerializer(post, data=data, partial=True)  #? Validate data 
        if serializer.is_valid():
            serializer.save()   #? Save serialized data
            return Response(serializer.data, status=status.HTTP_200_OK) #? Return JSON data 
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)   #? Return errors after validation

@api_view(['GET'])
@permission_classes([IsAuthenticated])
#?  'posts/categories/'
def CategoriesListView(request, format=None): #* Returns list of categories
    if request.method == 'GET':
        categories = PostCategory.objects.all()
        serializer = CategoriesListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
#?  'posts/<slug:category_slug>/<slug:post_slug>/reactions/'
def PostReactionsListView(request, category_slug, post_slug, format=None):#* Getting reactions, adding new reactions and updates users reaction
#* for specified user
    try:
        post = Post.objects.filter(category__slug=category_slug).get(slug=post_slug)
    except Post.DoesNotExist:
        return Response({"errors": {"post": "Nie znaleziono posta"}},status=status.HTTP_404_NOT_FOUND)
    print(post)
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
        serializer = ReactionPostSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    if request.method == 'PUT':
        try: 
            reaction = PostReaction.objects.filter(post=post).filter(user=request.user).get()
        except PostReaction.DoesNotExist:
            return Response(data={"errors": {"Reaction": "Reaction Do not Exists"}},status=status.HTTP_409_CONFLICT)
        data = request.data 
        data['user'] = request.user.id 
        data['post'] = post.id 
        
        serializer = ReactionPostSerializer(reaction,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    if request.method == 'DELETE':
        try: 
            reaction = PostReaction.objects.filter(post=post).filter(user=request.user).get()
        except PostReaction.DoesNotExist:
            return Response(data={"errors": {"Reaction": "Reaction Do not Exists"}},status=status.HTTP_409_CONFLICT)
        data = request.data 
        data['user'] = request.user.id 
        data['post'] = post.id 
        data['deleted'] = True
        
        serializer = ReactionPostSerializer(reaction,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
#?  'posts/<slug:category_slug>/<slug:post_slug>/reactions/me/'
def UserPostReactionsView(request,category_slug,post_slug, format=None):#*Post reactions of authenticated user
    try:
        post = Post.objects.filter(category__slug=category_slug).get(slug=post_slug)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        try:
            reactions = PostReaction.objects.filter(post= post).get(user= request.user.id)
        except:
            return Response(data={"errors": {"reactions": "Do not found"}}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReactionListSerializer(reactions)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#?  'posts/reactions/'
def PostsReactionsListView(request, format=None):#*Get All reactions
    if request.method == 'GET':
        reactions = PostReaction.objects.all()
        serializer = ReactionListSerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
#?  'posts/reactions/me/'
def UserPostsReactionsView(request,format=None):#* All reactions of specified user
    
    reactions = PostReaction.objects.filter(user=request.user)
    if not reactions.exists():
        return Response(data={"errors": {"reactions": "Do not found"}},status=status.HTTP_404_NOT_FOUND)
    serializer = ReactionListSerializer(reactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
#? 'posts/<slug:category_slug>/<slug:post_slug>/comments/'
def PostCommentListView(request, category_slug, post_slug, format=None):#* Comments of requested post

    try:    #? Check if requestet post exists
        post = Post.objects.filter(category__slug = category_slug).get(slug= post_slug)
    except Post.DoesNotExist:   #? If not return error 
        return  Response(data={"errors": {"post": "Does not exists"}},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        try: #? Try to find any not deleted comments
            comments = PostComment.objects.filter(post = post).filter(deleted=False)   
        except PostComment.DoesNotExist:    #? If not return error
            return HttpResponse(data={"errors": {"comment": "Do not found"}},status=status.HTTP_404_NOT_FOUND)
        #?  Serialize filtered data and return to requesting client 
        serializer = PostCommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        #? fetch request body data
        data = request.data
        data['user'] = request.user.id  #? Assign authorized user
        data['post'] = post.id #? Assign to specified post
        serializer = PostCommentListSerializer(data= data)  #? Serialize data
        if serializer.is_valid():   #? If there is no errors
            serializer.save()   #? Save and return new comment
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['GET','PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
#?  'posts/comments/<int:pk>/'
def PostCommentDetailView(request, pk, format=None): #* Detailed data of comment specified by comment id

    try:
        postcomment = PostComment.objects.get(pk=pk)
    except PostComment.DoesNotExist:
        return Response(data={"errors": {"post": "Do not found"}},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostCommentListSerializer(postcomment)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    if request.method == 'PUT':
        data = request.data
        data['user'] = request.user.id 
        
        data['post'] = postcomment.post.id
        serializer = PostCommentListSerializer(postcomment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'DELETE':
        if not postcomment.user.id == request.user.id:
            return Response(data={"errors": {"user": "permission deneied"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = {}
        data['user'] = request.user.id
        data['deleted'] = True 
        serializer = PostCommentListSerializer(postcomment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
#?  'posts/<slug:category_slug>/'
def PostCategoryListView(request, category_slug, format=None):#* Return posts of specified category

    category_posts = Post.objects.filter(category__slug=category_slug).all()
    if not category_posts.exists():
        return Response(data={"errors":{"Posts": "No posts found"}})
        
    if request.method == 'GET':
        serializer = PostDetailSerializer(category_posts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def PostsCommentsListView(request, foramt=None):
#     comments = PostComment.objects.all()
#     serializer = PostCommentListSerialzier(comments, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

