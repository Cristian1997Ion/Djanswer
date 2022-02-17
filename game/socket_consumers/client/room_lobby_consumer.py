import json
from channels.generic.websocket import AsyncWebsocketConsumer
from game.models import Player, Room
from channels.db import database_sync_to_async

import game.socket_consumers.utils as socket_utils

class RoomLobbyConsumer(AsyncWebsocketConsumer):    
    @database_sync_to_async
    def initialize(self):
        self.player: Player = self.scope['user']
        self.room: Room = Room.objects.select_related('owner').prefetch_related('players').get(pk=self.player.room_id)
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = socket_utils.get_lobby_channel_name()
        
        if self.room.game_started:
            raise Exception
        
        if self.room.code != self.room_code:
            raise Exception
        

    async def connect(self):
        await self.initialize()

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
                    'type': 'player_connected',
                    'user': self.player.username,
                }
            )
        elif data['type'] == 'chat_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message_received',
                    'text': data['text'],
                    'user': self.player.username
                }
            )
            
        return data

    async def player_connected(self, event):
        await self.send(text_data=json.dumps(event))

    async def chat_message_received(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def game_started(self, event):
        await self.send(text_data=json.dumps(event))
        