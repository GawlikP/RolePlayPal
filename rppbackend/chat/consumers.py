import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token
from games.models import Game
import re


@database_sync_to_async
def get_user(token):
    try:
        token = Token.objects.get(key=token)
        return token.user
    except Token.DoesNotExist:
        return "error"
@database_sync_to_async
def get_room_data(room_key, user):
    try:
        game = Game.objects.get(room_key= room_key)
        
    except Game.DoesNotExist:
        return "error"
    if user in game.players.all():
            return game
    if user.id == game.game_master.id:
        print("game master")
        return game
    return "error"
class ChatConsumer(AsyncWebsocketConsumer):

    username = "None"
    user = None
    game = None
    #room_group_name = ""

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_key']
        self.room_group_name = 'chat_%s' % 'test'



        query = dict((x.split('=') for x in self.scope['query_string'].decode().split("&")))
        self.user = await get_user(query['authorization'])

        if isinstance(self.user, str):
            print("papa")
            print(str)
            await self.disconnect(402)
            return
        self.game = await get_room_data(self.room_name, self.user)
        
        if isinstance(self.game, str):
            print("papa game")
            await self.disconnect(406)
            return
        self.room_group_name = 'chat_%s' % self.game.slug
        #self.room_group_name = 'chat_%s' % self.game.name


        self.scope["session"]["seed"] = random.randint(1,9999)
        self.scope["session"]["username"] = self.user.username
        self.scope["session"]["authorization"] = query['authorization']
        self.scope["session"]["game"] = self.game
        self.scope["session"]["user_id"] = self.user.id
      

       
        
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


        f = re.fullmatch(r"/r\s\d+d\d+", message)

        if f != None:
            nums = re.findall(r'\d+',message)
        
            rolls = []
            message = ""
            for i in range(0,int(nums[0])):
                rolls.append(random.randint(0,int(nums[1])))
            iterator = 1
            for v in rolls:
                message += f'ROLL({iterator}):{v} \n'
                iterator += 1

        data= {}

        data['message'] = message
        data['username'] = self.scope["session"]["username"]
        data['user_id'] = self.scope["session"]["user_id"]

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
