from django.urls import path
from .views import GameListView, GameDetailSlugView, GameGameInvitationsListView#, GameInvitationsListView, GameInvitationsMeView

urlpatterns = [
    path('', GameListView, name='get list and post endpoint'),
    path('<slug:game_slug>/', GameDetailSlugView, name='get detail get and put endpoint'),
    path('<slug:game_slug>/invitations/',GameGameInvitationsListView, name='get invitations by game_slug' )
   # path('invitations/', GameInvitationsListView),
   # path('invitations/me/',GameInvitationsMeView)
]