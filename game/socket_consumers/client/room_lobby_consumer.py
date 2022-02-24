import json
from channels.generic.websocket import AsyncWebsocketConsumer
from game.models import Player, Room
from channels.db import database_sync_to_async

import game.socket_consumers.utils as socket_utils

class RoomLobbyConsumer(AsyncWebsocketConsumer):    
    @database_sync_to_async
    def initialize(self):
        self.player: Player = self.scope['user']
        self.room: Room = Room.objects.select_related('owner').prefetch_related('player_set').get(pk=self.player.room_id)
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = socket_utils.get_lobby_channel_name(self.room_code)
        
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
        await self.send(text_data=json.dumps({
            'type': 'connected',
            'players': [player.username for player in self.room.player_set.all()]
        }))

    async def disconnect(self, code):
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
                    'player': self.player.username,
                }
            )
        elif data['type'] == 'chat_message':
            text: str = data['text']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message_received',
                    'text': text.strip(),
                    'player': self.player.username
                }
            )
        elif data['type'] == 'left':
            await self.leave_room()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_left',
                    'player': self.player.username
                }
            )
                
        return data
    
    @database_sync_to_async
    def leave_room(self):
        self.player.room = None
        self.player.save()

    async def player_connected(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def player_left(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def room_deleted(self, event):
        await self.send(text_data=json.dumps(event))


    async def chat_message_received(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def game_started(self, event):
        await self.send(text_data=json.dumps(event))
        