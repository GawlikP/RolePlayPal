from django.urls import re_path

from . import game_room_consumers, private_chat_consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_key>\w+)/$', game_room_consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/private/(?P<chat_name>\w+)/$', private_chat_consumers.ChatConsumer.as_asgi()),
]
