from django.urls import path
from .views import GameListView, GameDetailSlugView, GameGameInvitationsListView, GameGameInvitationsDetailView,GameGameInvitationsMeListView
from .views import GameGameInvitationsAccept, GamePlayersListView, GameGameInvitationsCancel, UsersGameListView
from .views import NewUsersGameInvitation, RemovePlayerFromGame, GameRoomKeyDetailView, GameHandoutDetailView
from .views import GameHandoutsListView
urlpatterns = [
    path('', GameListView, name='get list and post endpoint'),
    path('me/', UsersGameListView, name='get user games'),
    path('<slug:game_slug>/', GameDetailSlugView, name='get detail get and put endpoint'),
    path('<slug:game_slug>/players/', GamePlayersListView, name=' get list of game players'),
    path('<slug:game_slug>/invitations/',GameGameInvitationsListView, name='get invitations by game_slug' ),
    path('<slug:game_slug>/players/<int:player_id>/remove/', RemovePlayerFromGame, name=' remove player from players list'),
    path('<slug:game_slug>/handouts/', GameHandoutsListView, name='get all game handouts'),
    path('<slug:game_slug>/handouts/<slug:handout_slug>/',GameHandoutDetailView, name=' game handout post, get and put'),
    path('invitations/<int:pk>/', GameGameInvitationsDetailView, name='get and put for pk GameInvitations'),
    path('invitations/me/', GameGameInvitationsMeListView, name='get all my invitations'),
    path('invitations/<int:pk>/accept/', GameGameInvitationsAccept, name='user accepts invitation endpoint'),
    path('invitations/<int:pk>/cancel/', GameGameInvitationsCancel, name='user canceled invitation endpoint'),
    path('<int:game_id>/invitations/new/', NewUsersGameInvitation, name='get users allowed to add and post new invitation'),
    path('room_key/<str:room_key>/', GameRoomKeyDetailView, name='get game information by room key')
   # path('invitations/', GameInvitationsListView),
   # path('invitations/me/',GameInvitationsMeView)
]