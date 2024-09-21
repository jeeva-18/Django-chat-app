import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Messages, Room

from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s'% self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self,text_data):
        data = json.loads(text_data)
        username = data['username']
        message = data['message']
        room = data['room']

        await self.save_messages(username,room,message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'username' : username,
                'room' : room,
                'message' : message
            }
        )
    async def chat_message(self,event):
        username = event['username']
        message = event['message']
        room = event['room']

        await self.send(text_data = json.dumps({
            'username' : username,
            'room' : room,
            'message' : message
        })) 

    @sync_to_async
    def save_messages(self,username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Messages.objects.create(user=user,room=room,content=message)


