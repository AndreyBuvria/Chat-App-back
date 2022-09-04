import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core import serializers

from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.room = await database_sync_to_async(self.defineRoom)()
        self.messages = await database_sync_to_async(self.getMessages)()

        await self.accept()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        #await self.send(self.messages)

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'user_name': self.scope['user'].username,
                'room_id': self.room_name,
                'message': text_data.replace('"', ''),
            } 
        )

    async def chat_message(self, event):
        user = await self.getUser(event)
        msg = await self.createMessage(event, user)

        # Getting date and converting this to string
        timestamp = (getattr(msg, 'timestamp')).isoformat()
        
        await self.send(text_data=json.dumps({
            'user': event['user_name'],
            'room': event['room_id'],
            'text': event['message'],
            'date': timestamp
        }))
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # accessing to database through async
    def defineRoom(self):
        try:
            return Room.objects.get(name=self.room_name)
        except:
            return Room.objects.create(name=self.room_name)

    def getMessages(self):
        return serializers.serialize('python', Message.objects.filter(room=self.room))

    @database_sync_to_async 
    def getUser(self, event):
        return User.objects.get(username=event['user_name'])

    @database_sync_to_async
    def createMessage(self, event, user):
        return Message.objects.create(name=user, room=self.room, text=event['message'])

