import json
from channels.generic.websocket import AsyncWebsocketConsumer
from game.models import Player, Room
from channels.db import database_sync_to_async
from django import db

class RoomLobbyConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def initialize(self):
        self.user: Player = self.scope['user']
        self.room: Room = Room.objects.select_related('owner').prefetch_related('players').get(pk=self.user.room_id)
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_code
    
    async def connect(self):
        await self.initialize()
        if self.room.code != self.room_code:
            raise Exception('You are not in this room')


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'connected':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': data['type'],
                    'user': self.user.username,
                }
            )
        elif data['type'] == 'chat_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': data['type'],
                    'text': data['text'],
                    'user': self.user.username
                }
            )

    async def connected(self, event):
        await self.send(text_data=json.dumps(event))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

        