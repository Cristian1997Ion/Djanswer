from distutils.debug import DEBUG
import logging
import os
from typing import Final


class RoomLoggerBuilder(): 
    PATH: Final = 'game/room_logs'
    LEVEL: Final = 'INFO'
    
    def build(self, room_id):
        logger = logging.Logger(__name__)
        logger.setLevel(self.LEVEL)
        logger.addHandler(logging.FileHandler(os.path.join(self.PATH, f'{room_id:d}.log'), 'w'))
        
        return logger