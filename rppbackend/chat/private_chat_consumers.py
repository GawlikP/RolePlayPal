import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token
from games.models import Game

from profiles.models import Profile 
from private_messages.models import PrivateMessage
import re


@database_sync_to_async
def get_user(token):
    try:
        token = Token.objects.get(key=token)
        return token.user
    except Token.DoesNotExist:
        return "error"

@database_sync_to_async
def get_receiver_profile(user2):
    try: 
        profile = Profile.objects.get(slug=user2)
        return profile.user 
    except Profile.DoesNotExist:
        return "cannot get receiver profile"

@database_sync_to_async
def store_message(text,sender,receiver):
    try:
        message = PrivateMessage(text=text, sender_user=sender, receiver_user=receiver, readed=True)
        message.save()
        return message
    except PrivateMessage.DoesNotExist:
        return "cannot add message"

@database_sync_to_async
def get_thumbnail(user):
    try:
        profile = Profile.objects.get(user=user)
        return profile.get_thumbnail()
    except Profile.DoesNotExist:
        return 0

class ChatConsumer(AsyncWebsocketConsumer):

    username = "None"
    user = None

    #room_group_name = ""

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chat_name']
        #self.room_group_name = 'chat_%s' % 'test'



        query = dict((x.split('=') for x in self.scope['query_string'].decode().split("&")))
        self.user = await get_user(query['authorization'])

        if isinstance(self.user, str):
            print("papa")
            print(self.user)
            await self.disconnect(402)
            return
       
        
        self.receiver = await get_receiver_profile(query['user2'])

        if isinstance(self.receiver, str):
            print(self.receiver)
            await self.disconnect(402)
            return
        
        if not 'user1' in query or not 'user2' in query:
            await self.disconnect(402)
            return 

        thumbnail = await get_thumbnail(self.user)
        if isinstance(thumbnail, int):
            print("cannot fetch users thunbnail")
            await self.disconnect(402)
            return

        players = []
        players.append(query['user1'])
        players.append(query['user2'])
        print(players)
        players.sort()
        print(players)
        players = ''.join(players)
        print(players)
        self.room_group_name = 'chat_%s' % players


        self.scope["session"]["seed"] = random.randint(1,9999)
        self.scope["session"]["username"] = self.user.username
        self.scope["session"]["authorization"] = query['authorization']
        self.scope["session"]["user_id"] = self.user.id
        self.scope["session"]["receiver"] = self.receiver
        self.scope["session"]["sender"] = self.user
        self.scope["session"]["thumbnail"] = thumbnail
   
      

       
        
        #self.channel_name = 'chat_%s' % self.game.room_key

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
    
        


      

        data= {}

        data['message'] = message
        data['username'] = self.scope["session"]["username"]
        data['user_id'] = self.scope["session"]["user_id"]
        #data['sender'] = self.scope["session"]["sender"].id
        #data['receiver'] = self.scope["session"]["receiver"].id
        data['thumbnail'] = self.scope["session"]["thumbnail"]
        msg = await store_message(message, self.scope["session"]["sender"], self.scope["session"]["receiver"])
        if isinstance(msg, str):
            print(msg)

        

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data,
           
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
