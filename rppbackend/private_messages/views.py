from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser 
from rest_framework import serializers, status 
from rest_framework.response import Response 
from .models import PrivateMessage, MessageCredential
from django.db.models import Q 

from .serializers import PrivateMessageListSerializer, PrivateMessagePostSerializer,  MessageCredentialListSerializer, MessageCredentialPostSerializer
from profiles.models import Profile
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def PrivateMessageListView(request, format=None):
    if request.method == 'GET':
        privatemessages = PrivateMessage.objects.all()
        serializer = PrivateMessageListSerializer(privatemessages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data 
        data['sender_user'] = request.user.id
        serializer = PrivateMessagePostSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def PrivateMessageDetailView(request, pk, format=None):
    try:
        privatemessage = PrivateMessage.objects.get(pk = pk)
    except PrivateMessage.DoesNotExist:
        return Response(data={"errors": {"private_message": "Does not exists"}})

    if request.method == 'GET':
        serializer = PrivateMessageListView(privatemessage)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        data = request.data 
        data['receiver'] = request.user 
        serializer = PrivateMessagePostSerializer(privatemessage, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserPrivateMessagesListView(request, format=None):
    privatemessages = PrivateMessage.objects.filter((Q(receiver_user=request.user)) | (Q(sender_user=request.user)))

    if not privatemessages.exists():
        return Response(data={"errors": {"private_messages": "Nothing to show"}}, status=status.HTTP_404_NOT_FOUND)

    serializer = PrivateMessageListSerializer(privatemessages.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def UserPrivateMessagesWithProfileListView(request, profile_slug, format=None):
    try: 
        profile = Profile.objects.get(slug=profile_slug)
    except Profile.DoesNotExist:
        return Response(data={"errors": {"sender_user": "Does not exists"}})
    
    if request.method == 'GET':
        privatemessages = PrivateMessage.objects.filter((Q(receiver_user=request.user,sender_user=profile.user)) | (Q(sender_user=request.user, receiver_user=profile.user))).order_by('created')
        if not privatemessages.exists():
            return Response(data={"errors": {"private_messages": "Nothing to show"}}, status=status.HTTP_200_OK)

        serializer = PrivateMessageListSerializer(privatemessages.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data 
        data['sender_user'] = request.user.id
        data['receiver_user'] = profile.user.id
        serializer = PrivateMessagePostSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def MessageCredentialListView(request, format=None):
    if request.method == 'GET':
        messagecredentials = MessageCredential.objects.all()
        serializer = MessageCredentialListSerializer(messagecredentials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data 
        data['user_from'] = request.user.id 

        if MessageCredential.objects.filter(user_from=request.user).filter(user_to__id=data['user_to']).exits():
            return Response({"errors": {"message_credential": "Already Exists"}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = MessageCredentialPostSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def MessageCredentialDetailView(request,pk, format=None):
    try: 
        messagecredential = MessageCredential.objects.get(pk=pk)
    except MessageCredential.DoesNotExist:
        return Response({"error": {"message_credential": "Nothing to show"}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageCredentialListSerializer(messagecredential)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        data = request.data 
        if messagecredential.user_from.id != request.user.id:
            return Response({"errors":{"user": "Permission denaied"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
        serializer = MessageCredentialPostSerializer(messagecredential,data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def UserMessageCredentialListView(request, format=None):
    try:
        messagecredentials = MessageCredential.objects.filter(user_from=request.user).all()
    except MessageCredential.DoesNotExist:
        return Response({"errors": {"message_credential": "Nothing to show"}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageCredentialListSerializer(messagecredentials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data 
        data['user_from'] = request.user.id

        mc = MessageCredential.objects.filter(user_from=request.user).filter(user_to__id=data['user_to']).all()
        if mc.exists():
            return Response({"errors": {"message_credential": "Already Exists"}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = MessageCredentialPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def UserMessageCredentialProfileDetailView(request, profile_slug, format=None):
    try: 
        profile = Profile.objects.get(slug=profile_slug)
    except Profile.DoesNotExist:
        return Response(data={"errors":{"profile": "Does not exits"}}, status=status.HTTP_404_NOT_FOUND)
    try:
        messagecredential = MessageCredential.objects.filter(user_from=request.user).get(user_to=profile.user)
    except MessageCredential.DoesNotExist:
        return Response({"errors": {"messagecredential": "Does not exists"}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageCredentialListSerializer(messagecredential)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = request.data 
        data['user_from'] = request.user.id 
        data['user_to'] = profile.user.id
        serializer = MessageCredentialPostSerializer(messagecredential,data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

