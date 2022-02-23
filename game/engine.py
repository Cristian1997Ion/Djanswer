from random import shuffle
import threading
import time
import logging
from asgiref.sync import async_to_sync
from django.utils.timezone import now
from channels.layers import get_channel_layer
from dependency_injector.wiring import inject, Provide


from game.models import Room, Round, Question, Answer
from game.socket_consumers.utils import get_game_channel_name
from game.loggers import RoomLoggerBuilder
from game.containers import Container   

class GameEngine(threading.Thread):
    @inject
    def __init__(self, room_id, room_logger_builder: RoomLoggerBuilder = Provide(Container.room_logger_builder), **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.room: Room = Room.objects.prefetch_related('rounds', 'players').get(pk=room_id)
        self.room_group_name = get_game_channel_name(self.room.code)
        self.current_round = self.room.current_round
        self.channel_layer = get_channel_layer()
        self.logger: logging.Logger = room_logger_builder.build(room_id)
        
    def run(self):
        self.__question_phase()
        self.__answers_phase()
    
    def __question_phase(self):
        self.logger.info(f'STARTED QUESTIONS PHASE')
        self.current_round.questions_phase_started_at = now()
        self.current_round.save()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "questions_phase_started"})

        time.sleep(Round.QUESTIONS_PHASE_DURATION)

        # set a random question for players that didn't submit a question
        if self.current_round.questions.count() < self.room.players.count():
            for player in self.room.players.all():
                if not self.current_round.questions.filter(author=player).first():
                    Question(text='Random question', author=player, round=self.current_round).save()
        
        # determine which players answer which question
        available_respondests = list(self.room.players.all())
        shuffle(available_respondests)
        for index, respondent in enumerate(available_respondests):
            question = self.current_round.questions.get(author=available_respondests[index-1])
            question.respondent = respondent
            question.save()
        
        self.logger.info(f'ENDED QUESTIONS PHASE')

    def __answers_phase(self):
        self.logger.info(f'STARTED ANSWERS PHASE')
        self.current_round.answers_phase_started_at = now()
        self.current_round.save()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'answers_phase_started'})
        
        time.sleep(Round.ANSWERS_PHASE_DURATION)
        
        for question in self.current_round.questions.filter(answer=None):
            Answer(
                text="I don't know how to respond to that...",
                player=question.respondent,
                question=question
            ).save()
        
        self.logger.info(f'ENDED ANSWERS PHASE')
