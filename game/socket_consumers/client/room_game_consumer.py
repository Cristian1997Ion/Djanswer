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
        
        self.current_round = self.room.current_round

    async def connect(self):
        await self.initialize()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.determine_phase()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        
    async def determine_phase(self):
        if self.current_round is None:
            return
        
        if self.current_round.vote_phase_started_at:
            pass
        
        if self.current_round.answers_phase_started_at:
            pass
        
        if self.current_round.questions_phase_started_at:
            await self.questions_phase_started({
                'type': 'question_phase_started',
            })
        
    async def questions_phase_started(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'remaining_time': self.current_round.get_questions_phase_remaining_time()
        }))