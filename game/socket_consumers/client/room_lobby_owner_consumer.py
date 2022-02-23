import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from game.models.player import Player
from game.socket_consumers.client import RoomLobbyConsumer
from game.socket_consumers.utils import GAME_ENGINE_NAME

class RoomLobbyOwnerConsumer(RoomLobbyConsumer):

    @database_sync_to_async
    def initialize(self):
        async_to_sync(super(RoomLobbyOwnerConsumer, self).initialize)()
        if self.room.owner != self.player:
            raise Exception
    
    async def connect(self):
        await super(RoomLobbyOwnerConsumer, self).connect()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'left':
            await self.delete_room()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_deleted'
                }
            )
            
            return            
        elif data['type'] == 'start_game':
            if (not await self.start_game()):
                await self.channel_layer.send(
                    GAME_ENGINE_NAME,
                    {
                        'type': 'start_game_aborted',
                        'room_id': self.room.pk
                    }
            )

            await self.channel_layer.send(
                GAME_ENGINE_NAME,
                {
                    'type': 'start_game',
                    'room_id': self.room.pk
                }
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_started',
                }
            )
            
            return

        await super().receive(text_data)
    
    async def player_left(self, event):
        await self.send(text_data=json.dumps({'type': 'start_game_aborted'}))
        await super().player_left(event)
    
    @database_sync_to_async
    def delete_room(self):
        self.room.delete()
        

    @database_sync_to_async
    def start_game(self):
        if Player.objects.filter(room=self.room).count() < 4:
            return False

        self.room.game_started = True
        self.room.save()
        return True
        