from channels.consumer import SyncConsumer
from game.engine import GameEngine

class GameEngineConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def start_game(self, event):
        if not event['room_id']:
            return

        engine = GameEngine(event['room_id'])
        engine.start()
        