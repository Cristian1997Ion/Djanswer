from game.engine import GameEngine
from channels.consumer import SyncConsumer


class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = "snek_game"
        self.engine = GameEngine(self.group_name)
        self.engine.start()