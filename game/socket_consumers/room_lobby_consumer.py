import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomLobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

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
                    'type': 'connected',
                    'user': self.user.username,
                }
            )

    async def connected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'connected',
            'user': event['user']
        }))

        