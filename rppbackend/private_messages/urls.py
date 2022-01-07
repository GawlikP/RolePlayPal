from django.urls import path 
from .views import PrivateMessageListView, PrivateMessageDetailView, UserPrivateMessagesListView, UserPrivateMessagesWithProfileListView
from .views import MessageCredentialListView, MessageCredentialDetailView, UserMessageCredentialListView, UserMessageCredentialProfileDetailView
urlpatterns = [
    path('', PrivateMessageListView, name='get list of private messages '),
    path('<int:pk>/', PrivateMessageDetailView, name='get datail of private message or update private message'),
    path('me/', UserPrivateMessagesListView, name=' get list of requesting users private messages'),
    path('me/profile/<slug:profile_slug>/', UserPrivateMessagesWithProfileListView, name='get list of requesting users and specified user conversation messages'),
    path('messagecredentials/', MessageCredentialListView, name='get list of message credentials post new credential'),
    path('messagecredentials/<int:pk>/', MessageCredentialDetailView, name='get specified message credential data or put new message credential data'),
    path('messagecredentials/me/', UserMessageCredentialListView,  name='get list of message credentials for specified user or post new credential for this user'),
    path('messagecredentials/me/profile/<slug:profile_slug>/', UserMessageCredentialProfileDetailView, name='get message credential from specified user to specified profile or put new data'),

]