from django.urls import path
from .views import GameListView, GameDetailSlugView, GameGameInvitationsListView, GameGameInvitationsDetailView,GameGameInvitationsMeListView
from .views import GameGameInvitationsAccept, GamePlayersListView, GameGameInvitationsCancel, UsersGameListView
urlpatterns = [
    path('', GameListView, name='get list and post endpoint'),
    path('me/', UsersGameListView, name='get user games'),
    path('<slug:game_slug>/', GameDetailSlugView, name='get detail get and put endpoint'),
    path('<slug:game_slug>/players/', GamePlayersListView, name=' get list of game players'),
    path('<slug:game_slug>/invitations/',GameGameInvitationsListView, name='get invitations by game_slug' ),
    path('invitations/<int:pk>/', GameGameInvitationsDetailView, name='get and put for pk GameInvitations'),
    path('invitations/me/', GameGameInvitationsMeListView, name='get all my invitations'),
    path('invitations/<int:pk>/accept/', GameGameInvitationsAccept, name='user accepts invitation endpoint'),
    path('invitations/<int:pk>/cancel/', GameGameInvitationsCancel, name='user accepts invitation endpoint'),
   # path('invitations/', GameInvitationsListView),
   # path('invitations/me/',GameInvitationsMeView)
]