import threading

class GameEngine(threading.Thread):
    def __init__(self, room_group_name, **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.room_group_name = room_group_name