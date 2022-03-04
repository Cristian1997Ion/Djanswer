import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from game.models import Player, Room
from game.socket_consumers import utils as socket_utils

class RoomLobbyConsumer(WebsocketConsumer):    
    def initialize(self):
        self.player: Player = self.scope["user"]
        self.room: Room = Room.objects.select_related("owner").prefetch_related("player_set").get(pk=self.player.room_id)
        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        self.room_group_name = socket_utils.get_lobby_channel_name(self.room_code)
        
        if self.room.game_started:
            self.close()
        
        if self.room.code != self.room_code:
            self.close()
        

    def connect(self):
        self.initialize()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            "type": "connected",
            "players": [player.username for player in self.room.player_set.all()]
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "connect":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "player_connected",
                    "player": self.player.username,
                }
            )
        elif data["type"] == "chat_message":
            text: str = data["text"]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message_received",
                    "text": text.strip(),
                    "player": self.player.username
                }
            )
        elif data["type"] == "left":
            self.player.room = None
            self.player.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "player_left",
                    "player": self.player.username
                }
            )
                
        return data

    def player_connected(self, event):
        self.send(text_data=json.dumps(event))
        
    def player_left(self, event):
        self.send(text_data=json.dumps(event))
        
    def room_deleted(self, event):
        self.send(text_data=json.dumps(event))

    def chat_message_received(self, event):
        self.send(text_data=json.dumps(event))
        
    def game_started(self, event):
        self.send(text_data=json.dumps(event))
        