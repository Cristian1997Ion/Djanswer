import threading
import time
import logging
from django.utils.timezone import now
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from dependency_injector.wiring import inject, Provide


from game.models import Room
from game.models.round import Round
from game.socket_consumers.utils import get_game_channel_name
from game.loggers import RoomLoggerBuilder
from game.containers import Container   

class GameEngine(threading.Thread):
    @inject
    def __init__(self, room_id, room_logger_builder: RoomLoggerBuilder = Provide(Container.room_logger_builder), **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.room: Room = Room.objects.prefetch_related('rounds').get(pk=room_id)
        self.room_group_name = get_game_channel_name(self.room.code)
        self.current_round = self.room.current_round
        self.channel_layer = get_channel_layer()
        self.logger: logging.Logger = room_logger_builder.build(room_id)
        
    def run(self):
        self.logger.info(f'STARTED QUESTION PHASE')
        self.current_round.questions_phase_started_at = now()
        self.current_round.save()
        self.channel_layer.group_send(
            self.room_group_name,
            {"type": "question_phase_started"}
        )
        time.sleep(Round.QUESTIONS_PHASE_DURATION)

        self.logger.info(f'ENDED QUESTION PHASE ({self.current_round.questions.count()} questions)')
