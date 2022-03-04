import json
from asgiref.sync import async_to_sync
from game.models.player import Player
from game.socket_consumers.client import RoomLobbyConsumer
from game.socket_consumers.utils import GAME_ENGINE_NAME

class RoomLobbyOwnerConsumer(RoomLobbyConsumer):

    def initialize(self):
        super(RoomLobbyOwnerConsumer, self).initialize()
        if self.room.owner != self.player:
            self.close()
    
    def connect(self):
        super(RoomLobbyOwnerConsumer, self).connect()

    def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "left":
            self.room.delete()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "room_deleted"
                }
            )
            
            return            
        elif data["type"] == "start_game":
            if Player.objects.filter(room=self.room).count() < 4:
                async_to_sync(self.channel_layer.send)(
                    GAME_ENGINE_NAME,
                    {
                        "type": "start_game_aborted",
                        "room_id": self.room.pk
                    }
                )
                
                return

            self.room.game_started = True
            self.room.save()

            async_to_sync(self.channel_layer.send)(
                GAME_ENGINE_NAME,
                {
                    "type": "start_game",
                    "room_id": self.room.pk
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "game_started",
                }
            )
            
            return

        super().receive(text_data)
    
    def player_left(self, event):
        self.send(text_data=json.dumps({"type": "start_game_aborted"}))
        super().player_left(event)

        