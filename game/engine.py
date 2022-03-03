import threading, time, logging, urllib.parse
from asgiref.sync import async_to_sync
from django.utils.timezone import now
from channels.layers import get_channel_layer
from dependency_injector.wiring import inject, Provide
from matplotlib import pyplot
from matplotlib.figure import Figure
from io import BytesIO
from random import shuffle
from base64 import b64encode


from game.models import Room, Round, Question, Answer
from game.models.vote import Vote
from game.socket_consumers.utils import get_game_channel_name
from game.loggers import RoomLoggerBuilder
from game.containers import Container 

class GameEngine(threading.Thread):
    @inject
    def __init__(self, room_id, room_logger_builder: RoomLoggerBuilder = Provide(Container.room_logger_builder), **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.room: Room = Room.objects.prefetch_related("round_set", "player_set").get(pk=room_id)
        self.room_group_name = get_game_channel_name(self.room.code)
        self.current_round = self.room.get_current_round()
        self.channel_layer = get_channel_layer()
        self.logger: logging.Logger = room_logger_builder.build(room_id)
        self.scoreboard = Scoreboard()
        
    def run(self):
       # try:
            while self.current_round is not None:
                print('questions')
                self.__question_phase()
                print('answers')
                self.__answers_phase()
                print('votes')
                self.__vote_phase()
                print('summary')
                self.__round_summary()
                self.current_round = self.room.get_current_round()
            
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "game_ended", "winner": self.__determine_winner() })
        #except Exception as exception:
        #     self.logger.error(exception)
    
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
        self.scoreboard.update_round_scores(self.current_round)
        
    def __round_summary(self):
        self.current_round.ended = True
        self.current_round.save()
        
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            "type": "round_ended",
            "round_graphic": self.__create_bar_graphic(self.scoreboard.get_round_scores(self.current_round)),
            "overall_graphic": self.__create_bar_graphic(self.scoreboard.get_overall_scores())
        })

        time.sleep(5)
        
    def __create_bar_graphic(self, data: dict):
        room_fig: Figure = pyplot.figure()
        axes = room_fig.add_axes([0,0,1,1])
        axes.xaxis.label.set_color('white')
        axes.yaxis.label.set_color('white')
        axes.tick_params(axis='x', colors='white')
        axes.tick_params(axis='y', colors='white')
        axes.spines['left'].set_color('white')
        axes.spines['right'].set_color('white')
        axes.spines['top'].set_color('white')
        axes.spines['bottom'].set_color('white')
        container = axes.bar(data.keys(), data.values(), color="white")
        axes.bar_label(container, color="white")
        
        buffer = BytesIO()
        room_fig.savefig(buffer, dpi=300, bbox_inches="tight", transparent=True, format="png")
        buffer.seek(0)

        return urllib.parse.quote(b64encode(buffer.read()).decode())
        
    def __determine_winner(self) -> str:
        return next(iter(self.scoreboard.get_overall_scores()))
    
class Scoreboard():
    _scoreboard = {}
    
    def get_round_scores(self, round: Round) -> dict:
        return self.__sort_scores(self._scoreboard[round.pk])
    
    def get_overall_scores(self) -> dict:
        players_scores = {}
        for round_scores in self._scoreboard.values():
            round_scores: dict
            for player_name, player_score in round_scores.items():
                if not players_scores.get(player_name, False):
                    players_scores[player_name] = 0

                players_scores[player_name] += player_score
        
        return self.__sort_scores(players_scores)
    
    def update_round_scores(self, round: Round):
        self._scoreboard[round.pk] = {player.username:0 for player in round.room.player_set.all()}
        
        round_questions = (
            round.question_set
            .select_related("answer")
            .prefetch_related("answer__vote_set")
            .all()
        )
        
        
        answers_votes = {question.answer.pk: question.answer.vote_set.count() for question in round_questions}
        most_voted_answer_pk = max(answers_votes, key=answers_votes.get)
        
        most_voted_answer = round_questions.get(answer__pk=most_voted_answer_pk).answer
        self._scoreboard[round.pk][round.room.player_set.get(pk=most_voted_answer.player_id).username] += 2
        self._scoreboard[round.pk][round.room.player_set.get(pk=most_voted_answer.question.author_id).username] += 1
                
    def __sort_scores(self, scores: dict):
        return {
            player_name: player_score for player_name, player_score in sorted(scores.items(), key=lambda item: item[1], reverse=True)
        }
    
    