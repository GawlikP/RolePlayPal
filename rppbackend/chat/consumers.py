import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token

import re


@database_sync_to_async
def get_user(token):
    try:
        token = Token.objects.get(key=token)
        return token.user
    except Token.DoesNotExist:
        return "error"


class ChatConsumer(AsyncWebsocketConsumer):

    username = "None"
    user = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        print(f'{self.scope["user"]}')

        query = dict((x.split('=') for x in self.scope['query_string'].decode().split("&")))
        self.user = await get_user(query['authorization'])

        if isinstance(self.user, str):
            print("papa")
            await self.disconnect(402)
            return

        self.scope["session"]["seed"] = random.randint(1,9999)
        self.scope["session"]["username"] = self.user.username
        self.scope["session"]["authorization"] = query['authorization']
        print(f'{self.user.username}')


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
            print(nums)
            rolls = []
            message = ""
            for i in range(0,int(nums[0])):
                rolls.append(random.randint(0,int(nums[1])))
            iterator = 1
            for v in rolls:
                message += f'ROLL({iterator}):{v} \n'
                iterator += 1


        message = f'{self.scope["session"]["username"]}: {message}'

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
