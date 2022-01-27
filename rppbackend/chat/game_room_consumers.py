import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token
from games.models import Game
from profiles.models import Profile
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
        return game
    return "error"
@database_sync_to_async
def check_user_type(room_key, user):
    try:
        game = Game.objects.get(room_key= room_key)
        
    except Game.DoesNotExist:
        return "error"
    if user.id == game.game_master.id:
        return "yes"
    return "no"

@database_sync_to_async
def get_t(user):
    try: 
        profile = Profile.objects.get(user__id=user.id)
        return profile.get_thumbnail()
    except Profile.DoesNotExist:
        return 1



class ChatConsumer(AsyncWebsocketConsumer):

    username = "None"
    user = None
    game = None
    #room_group_name = ""

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_key']
        self.room_group_name = 'chat_%s' %  self.room_name



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
        game_master = await check_user_type(self.room_name, self.user)

        #self.room_group_name = 'chat_%s' % self.game.name

        profile = await get_t(self.user)
        if isinstance(profile, int):
            print(profile)
            await self.disconnect(402)
            return
        


        self.scope["session"]["seed"] = random.randint(1,9999)
        self.scope["session"]["username"] = self.user.username
        self.scope["session"]["authorization"] = query['authorization']
        self.scope["session"]["game"] = self.game
        self.scope["session"]["user_id"] = self.user.id
        self.scope["session"]["thumbnail"] =  profile
        print(self.scope["session"]["thumbnail"])
        
        if game_master == "yes":
            self.scope["session"]["game_master"] = True
        else:
            self.scope["session"]["game_master"] = False
      

       
        
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
        handout = ''
        if self.scope["session"]["game_master"] and 'handout' in text_data_json:
            handout = text_data_json['handout']
        
        

        data= {}

        f = re.fullmatch(r"/r(\s(\d+d?\d*)\s?\+?)*", message)

        if f != None:
            rolls = re.findall(r'\d+d\d+', message)
            print(f'rolls:{rolls}')
            numbers = re.findall(r'\s\d+(?!d)(?!\d+)\s?', message)
            print(f'numbers:{numbers}')
            nums = []
            for n in numbers:
                nums.append(int(re.sub(r'\s', '', n)))
            rolls_end = []
            rolls_new = []
            rolls_buffer = []
            message = ""
            how_many_rolls = []
            for i,r in enumerate(rolls):
                how_many_rolls.append(re.findall(r'\d+(?=d)', r))
            print(f'how_many:{how_many_rolls}')
            for i,x in enumerate(rolls):
                dice_type = ''
                for i in range(0,int(how_many_rolls[i][0])):
                    dice_type = re.sub(r'\d+d','', x)
                    print(f'dice_type[{i}]:' + str(dice_type))
                    rd = random.randint(1,int(dice_type))
                    rolls_end.append(rd)
                    rolls_buffer.append(rd)
                for r in rolls_buffer:
                    rolls_new.append(f'd{dice_type}')
                    rolls_buffer = []
            print("rolls_end" + str(rolls_end))
            print("rolls_new:" + str(rolls_new))
            iterator = 1
            for v in rolls_end:
                #message += f'ROLL({iterator} : {rolls[iterator-1]}):{v} \n'
                iterator += 1
            iterator = 0
            print("Nums:" + str(nums))
            for n in nums:
                message += f'ADD({iterator+1}): {n}\n'
                print("Number {interator}:" + str(n))
                iterator +=1
            result = 0 
            result += sum(rolls_end)
            if isinstance(nums, list):
                result += sum(nums)
            else:
                result += nums
            message += f'RESULT:{result}'

            data['result'] = result 
            data['rolls'] = rolls_new
            data['rolls_end'] = rolls_end
            data['numbers'] = nums

        

        data['message'] = message
        data['username'] = self.scope["session"]["username"]
        data['user_id'] = self.scope["session"]["user_id"]
        data['new_handout'] = handout
        data['thumbnail'] = self.scope["session"]["thumbnail"]

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
