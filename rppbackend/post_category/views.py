from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status
from rest_framework.rest_framework import Response 
from .models import Game
from .serializers import GameListSerializer 
from django.contrib.auth.models import User 


@api_view(['GET','POST'])
@permissions([IsAuthenticated])
def GameListView(request,format=None):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameListSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
