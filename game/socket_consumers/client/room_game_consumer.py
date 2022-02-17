import json
from channels.generic.websocket import AsyncWebsocketConsumer
from game.models import Player, Room, Round
from channels.db import database_sync_to_async
from django.db.models import Prefetch
import game.socket_consumers.utils as socket_utils

class RoomGameConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def initialize(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = socket_utils.get_game_channel_name(self.room_code)
        self.user: Player = self.scope['user']
        self.room: Room = (
            Room.objects
            .select_related('owner')
            .prefetch_related('players', Prefetch('rounds', queryset=Round.objects.order_by('id')))
            .get(pk=self.user.room_id)
        )
        
        if self.room.code != self.room_code:
            raise Exception
        
        self.currentRound = self.room.rounds.filter(ended_at=None).first()
        if self.currentRound is None:
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
        print(text_data)
        data = json.loads(text_data)
        