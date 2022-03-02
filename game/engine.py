import threading, time, logging, urllib.parse
from asgiref.sync import async_to_sync
from django.utils.timezone import now
from channels.layers import get_channel_layer
from dependency_injector.wiring import inject, Provide
from matplotlib import pyplot
from io import BytesIO
from random import shuffle
from base64 import b64encode

from game.models import Room, Round, Question, Answer
from game.socket_consumers.utils import get_game_channel_name
from game.loggers import RoomLoggerBuilder
from game.containers import Container 


from django.db import connection  

class GameEngine(threading.Thread):
    @inject
    def __init__(self, room_id, room_logger_builder: RoomLoggerBuilder = Provide(Container.room_logger_builder), **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.room: Room = Room.objects.prefetch_related("round_set", "player_set").get(pk=room_id)
        self.room_group_name = get_game_channel_name(self.room.code)
        self.current_round = self.room.current_round
        self.channel_layer = get_channel_layer()
        self.logger: logging.Logger = room_logger_builder.build(room_id)
        self.scoreboard = {}
        
    def run(self):
        try:
            while self.current_round is not None:
                print('questions')
                self.__question_phase()
                print('answers')
                self.__answers_phase()
                print('votes')
                self.__vote_phase()
                print('summary')
                return
                self.current_round = self.room.current_round
            
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "game_ended", "winner": self.determine_winner() })
        except Exception as exception:
            self.logger.error(exception)
    
    def __question_phase(self):
        self.logger.info("STARTED QUESTIONS PHASE")
        self.current_round.questions_phase_started_at = now()
        self.current_round.save()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "questions_phase_started"})

        time.sleep(Round.QUESTIONS_PHASE_DURATION)

        # set a random question for players that didn"t submit a question
        if self.current_round.question_set.count() < self.room.player_set.count():
            for player in self.room.player_set.all():
                if not self.current_round.question_set.filter(author=player).first():
                    Question(text="Random question", author=player, round=self.current_round).save()
        
        self.logger.info("ENDED QUESTIONS PHASE")

    def __answers_phase(self):
        self.logger.info("STARTED ANSWERS PHASE")
        
         # determine which players answer which question
        available_respondests = list(self.room.player_set.all())
        shuffle(available_respondests)
        for index, respondent in enumerate(available_respondests):
            question = self.current_round.question_set.get(author=available_respondests[index-1])
            question.respondent = respondent
            question.save()
        
        self.current_round.answers_phase_started_at = now()
        self.current_round.save()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "answers_phase_started"})
    
        
        time.sleep(Round.ANSWERS_PHASE_DURATION)
        for question in self.current_round.question_set.select_related("answer").filter(answer=None).all():
            Answer(
                text="I don't know how to respond to that...",
                player=question.respondent,
                question=question
            ).save()
        
        self.logger.info("ENDED ANSWERS PHASE")
        
    def __vote_phase(self):
        self.logger.info("START VOTE PHASE")
        self.current_round.vote_phase_started_at = now()
        self.current_round.save()
        
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "vote_phase_started"})
        time.sleep(Round.VOTE_PHASE_DURATION)
        
        self.scoreboard[self.current_round.pk] = {player.username:0 for player in self.room.player_set.all()}
        round_questions = (
            self.current_round.question_set
            .select_related("answer")
            .prefetch_related("answer__vote_set")
            .all()
        )
        
        for question in round_questions:
            for vote in question.answer.vote_set.all():
                self.scoreboard[self.current_round.pk][self.room.player_set.get(pk=vote.answer.player_id).username] += 2
                self.scoreboard[self.current_round.pk][self.room.player_set.get(pk=vote.answer.question.author_id).username] += 1
        
        for query in connection.queries:
            self.logger.info(query)
        
        self.current_round.ended = True
        self.current_round.save()
        
        players_names  = []
        players_scores = []
        current_round_scores: dict = self.scoreboard[self.current_round.pk]
        for player_name, player_score in current_round_scores.items():
            players_names.append(player_name)
            players_scores.append(player_score)
        
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            "type": "round_ended",
            "graph": self.create_bar_graphic(players_names, players_scores)
        })

        time.sleep(30)
        
    def create_bar_graphic(self, x_axis_data, y_axis_data):
        room_fig = pyplot.figure()
        axes = room_fig.add_axes([0,0,1,1])
        axes.bar(x_axis_data, y_axis_data)
        buffer = BytesIO()
        room_fig.savefig(buffer, dpi=300, bbox_inches='tight')
        buffer.seek(0)

        return urllib.parse.quote(b64encode(buffer.read()).decode())
        
    def determine_winner(self):
        player_scores = {player.username:0 for player in self.room.player_set.all()}
        for round_scores in self.scoreboard.values():
            round_scores: dict
            for player_name, player_score in round_scores.items():
                player_scores[player_name] += player_score
        
        return max(player_scores, key=player_scores.get)