from . import RoomLobbyConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

class RoomLobbyOwnerConsumer(RoomLobbyConsumer):

    @database_sync_to_async
    def initialize(self):
        async_to_sync(super(RoomLobbyOwnerConsumer, self).initialize)()
        if self.room.owner != self.player:
            raise Exception
    
    async def connect(self):
        await super(RoomLobbyOwnerConsumer, self).connect()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = await super().receive(text_data)
        if data['type'] == 'start_game':
            await self.start_game()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_started',
                }
            )

        return data
    
    @database_sync_to_async
    def start_game(self):
        self.room.game_started = True
        self.room.save()
        