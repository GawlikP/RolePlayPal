from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status
from rest_framework.response import Response    
from .models import Game, GameInvitation, GameHandout
from .serializers import GameListSerializer, GameInvitationListSerializer, GameInvitationPostSerializer, PlayerSerializer, GamePostSerializer
from .serializers import GameHandoutListSerializer
from django.contrib.auth.models import User 
from datetime import datetime
from profiles.models import Profile
from django.core.paginator import Paginator
from django.db.models import Q
from profiles.serializers import ProfileDetailSerializer


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

        serializer = GamePostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GamePlayersListView(request, game_slug, format=None):
    try: 
        game = Game.objects.get(slug= game_slug)
    except Game.DoesNotExist:
        return Response(data={"errors": { "profile": "Does not exist" }},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':


        serializer = PlayerSerializer(game.players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UsersGameListView(request, format=None):
    if request.method == "GET":
        #games = Game.objects.filter(game_master__id= request.user.id)#Game.objects.filter(players__id = request.user.id) #  
        games = Game.objects.filter(deleted=False).filter( Q(players__id = request.user.id) | Q(game_master__id = request.user.id)).distinct()
        
        if not games.exists():
            return Response(data={"errors": {"games": "Nothing to show"}}, status=status.HTTP_404_NOT_FOUND)
        
        page_number = request.query_params.get('page_number', 1)                       
        page_size = request.query_params.get('page_size',5) 

        paginator = Paginator(games, page_size)
        if int(page_number) > paginator.num_pages:
            return Response({'error': 'Page do not exist!'}, status=status.HTTP_404_NOT_FOUND)
        

        serializer = GameListSerializer(paginator.page(page_number), many=True)
        data = {}
        data['games'] = serializer.data 
        data['page_numbers'] = paginator.num_pages
        data['next_page'] = False if int(page_number) >= paginator.num_pages else True

        return Response(data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def GameDetailSlugView(request,game_slug,format=None):
    try: 
        game = Game.objects.get(slug= game_slug)
    except Game.DoesNotExist:
        return Response(data={"errors": { "profile": "Does not exist" }},status=status.HTTP_404_NOT_FOUND)

    
    if request.method == 'GET':
        serializer = GameListSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        if game.game_master.id != request.user.id:
            return Response({'error': 'Permission denaied'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = request.data
        print(data['deleted'])
        data['edited'] = datetime.now()
        
        if 'image' in data:
            print(data['image'])
            game.image.delete()
            game.image = data['image']
        
            game.save()
            
        
        serializer = GameListSerializer(game, data=data, partial=True)
        if serializer.is_valid():
           
            game = serializer.save()
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED     )
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GameRoomKeyDetailView(request, room_key, format=None):
    try: 
        game = Game.objects.get(room_key=room_key)
    except Game.DoesNotExist:
        return Response(data={"errors": {"game": "Does not exists"}}, status=status.HTTP_404_NOT_FOUND)
    
    if not request.user in game.players.all() and not request.user == game.game_master:
            return Response(data={"errors": {"user": "permission denaied"}}, status=status.HTTP_404_NOT_FOUND)
    serializer = GameListSerializer(game)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
        if not game.game_master.id == request.user.id:
            return Response(data={"errors": {"game_master": "premission_denaied"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = request.data
        if 'player_slug' in data:
            try:
                profile = Profile.objects.get(slug=data['player_slug'])
            except Profile.DoesNotExist:
                return Response(data={"errors": {"player_slug": "Profile Does No Exist"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            data['player'] = profile.user.id

        
        data['created'] = datetime.now()
        data['edited'] = datetime.now()
        data['game'] = game.id 
        data['game_master_sender'] = request.user.id

        if GameInvitation.objects.filter(game=game, player__id=data['player']).exists():
            return Response(data={"errors": {"invitation": "Already exists"}},status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = GameInvitationPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def GameGameInvitationsDetailView(request, pk, format=None):
    try:
        game_invitation = GameInvitation.objects.get(pk=pk)
    except GameInvitation.DoesNotExist:
        return Response(data={"errors": {"Game Invitation": "Dose not exist"}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GameInvitationListSerializer(game_invitation)
        if game_invitation.player.id == request.user.id:
            game_invitation.readed = True
            game_invitation.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        if game.game_master.id == request.user.id:
            return Response(data={"errors": {"game_master": "premission_denaied"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = request.data
        if 'player_slug' in data:
            try:
                profile = Profile.objects.get(slug=data['player_slug'])
            except Profile.DoesNotExist:
                return Response(data={"errors": {"player_slug": "Profile Does No Exist"}})
            data['player'] = profile.user.id
        data['edited'] = datetime.now()
        serializer = GameInvitationPostSerializer(game_invitation,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GameGameInvitationsMeListView(request, format=None):
    if request.method == "GET":

        

        my_game_invitations = GameInvitation.objects.filter(player__id=request.user.id)
        if not my_game_invitations.exists():
            return Response(data={"errors":{"player": "Dont have any invitations"}}, status=status.HTTP_404_NOT_FOUND)
        if request.GET.get('accepted'):
            my_game_invitations = my_game_invitations.filter(accepted=request.GET.get('accepted'))
        if request.GET.get('canceled'):
            my_game_invitations = my_game_invitations.filter(canceled=request.GET.get('canceled'))
        
        if not my_game_invitations.exists():
            return Response(data={"errors":{"invitations": "Nothing to show"}}, status=status.HTTP_404_NOT_FOUND)
        
        page_number = request.query_params.get('page_number', 1)                       
        page_size = request.query_params.get('page_size',5) 

        paginator = Paginator(my_game_invitations, page_size)
        if int(page_number) > paginator.num_pages:
            return Response({'error': 'Page do not exist!'}, status=status.HTTP_404_NOT_FOUND)

        #my_game_invitations.update(readed=True)

        serializer = GameInvitationListSerializer(paginator.page(page_number), many=True)
        
        data = {}
        data['invitations'] = serializer.data 
        data['page_numbers'] = paginator.num_pages
        data['next_page'] = False if int(page_number) >= paginator.num_pages else True

        return Response(data, status=status.HTTP_200_OK)

       

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def GameGameInvitationsAccept(request, pk, format=None):
    try:
        game_invitation = GameInvitation.objects.get(pk=pk)
    except GameInvitation.DoesNotExist:
        return Response(data={"errors": {"Game Invitation": "Dose not exist"}}, status=status.HTTP_404_NOT_FOUND)

    if not game_invitation.player.id == request.user.id:
        return Response(data={"errors": {"Player": "Do not have permission"}})

    if request.method == "POST":
        data = {}
        data['accepted'] = True
        data['readed'] = True
        
        serializer = GameInvitationListSerializer(game_invitation, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            game_invitation.game.players.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def GameGameInvitationsCancel(request, pk, format=None):
    try:
        game_invitation = GameInvitation.objects.get(pk=pk)
    except GameInvitation.DoesNotExist:
        return Response(data={"errors": {"Game Invitation": "Does not exist"}}, status=status.HTTP_404_NOT_FOUND)

    if not game_invitation.player.id == request.user.id:
        return Response(data={"errors": {"Player": "Do not have permission"}})

    if request.method == "POST":
        data = {}
        data['canceled'] = True
        data['readed'] = True
        
        serializer = GameInvitationListSerializer(game_invitation, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            game_invitation.game.players.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def NewUsersGameInvitation(request,game_id, format=True):
    try: 
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return Response(data={"errors":{"game": "Does not exist"}}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        if not request.user.id == game.game_master.id:
            return Response(data={"errors":{"user": "Permission denaied"}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        profiles = Profile.objects.filter(~Q(user__in = game.players.all())).filter(~Q(user__pk = game.game_master.id)).all()
        if request.GET.get('username'):
            profiles = profiles.filter((Q(user__username__contains=request.GET.get('username'))) | (Q(slug__contains=request.GET.get('slug'))) )
        if not profiles.exists():
            return Response(data={"errors": {"profiles": "No profiles to show"}})

        serializer = ProfileDetailSerializer(profiles, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def RemovePlayerFromGame(request, game_slug, player_id, format=None):
    try: 
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return Response(data={"errors":{"game": "Does not exist"}}, status=status.HTTP_404_NOT_FOUND)
    try:
        player = User.objects.get(pk=player_id)
    except User.DoesNotExist:
        return Response(data={"erors":{"player": "Does not exist"}}, status=status.HTTP_404_NOT_FOUND)
    if not request.user.id == game.game_master.id:
            return Response(data={"errors":{"user": "Permission denaied"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    if not player in game.players.all():
        return Response(data={"errors": {"player": "No player to remove"}}, status=status.HTTP_404_NOT_FOUND)

    game.players.remove(player)
    game.save()
    serializer = GameInvitationListSerializer(game)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def GameHandoutsListView(request, game_slug, format=None):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return Response(data={"errors": {"game": "Does not exists"}}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        handouts = GameHandout.objects.filter(game=game, deleted=False)
        serializer = GameHandoutListSerializer(handouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        if game.game_master.id != request.user.id:
            return Response({'error': {'game_master':'Permission denaied'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        game_handout = GameHandout()

        data = request.data
        game_handout.game = game
        game_handout.name = data['name']
        if 'image' in data:
  
            game_handout.image = data['image']
            game_handout.save()

        data['edited'] = datetime.now()
        serializer = GameHandoutListSerializer(game_handout, data=data,partial=True)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def GameHandoutDetailView(request, game_slug, handout_slug, format=None):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return Response(data={"errors": {"game": "Does not exists"}}, status=status.HTTP_404_NOT_FOUND)

    try:
        gamehandout = GameHandout.objects.filter(game=game).get(slug=handout_slug)
    except GameHandout.DoesNotExist:
        return Response(data={"errors": {"game_handout": "Does not exist"}}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = GameHandoutListSerializer(gamehandout)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        if game.game_master.id != request.user.id:
            return Response({'error': {'game_master':'Permission denaied'}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = request.data
        data['edited'] = datetime.now()
        serializer = GameHandoutListSerializer(gamehandout, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            
