import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q, Prefetch

from game.socket_consumers import utils as socket_utils
from game.models import Player, Room, Round, Answer, Question, Vote

class RoomGameConsumer(WebsocketConsumer):
    def initialize(self):
        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        self.room_group_name = socket_utils.get_game_channel_name(self.room_code)
        self.player: Player = self.scope["user"]
        self.room: Room = (
            Room.objects
            .select_related("owner")
            .prefetch_related("player_set", Prefetch("round_set", queryset=Round.objects.order_by("id")))
            .get(pk=self.player.room_id)
        )
        
        if self.room.code != self.room_code:
            raise Exception
        
        self.current_round = self.room.get_current_round()

    def connect(self):
        self.initialize()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.determine_phase()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "question":
            try:
                self.submit_question(data["text"]); 
            except:
                self.send(text_data=json.dumps({
                    "type": "question_error",
                    "error": "An error occured while submiting your question, please try again!",
                    "remaining_time": self.current_round.get_questions_phase_remaining_time()
                }))
            finally:
                return
        
        if data["type"] == "answer":
            try:
                self.submit_answer(data["text"])
            except:
                question: Question = self.get_assigned_question()
                self.send(text_data=json.dumps({
                    "type": "answer_error",
                    "error": "An error occured while submiting your answer, please try again!",
                    "remaining_time": self.current_round.get_answers_phase_remaining_time(),
                    "question": question.text
                }))
            finally:
                return
        
        if data["type"] == "vote":
            try:
                self.submit_vote(data["answer_id"])
            except Exception:
                self.send(text_data=json.dumps({
                    "type": "vote_error",
                    "error": "An error occured while submiting your vote, please try again!",
                }))
            finally:
                return
            
            return
            
    def determine_phase(self):
        if self.current_round is None:
            return
        
        if self.current_round.vote_phase_started_at is not None:
            self.vote_phase_started({"type": "vote_phase_started"})
            return
        
        if self.current_round.answers_phase_started_at is not None:
            self.answers_phase_started({"type": "answers_phase_started"})
            return
        
        if self.current_round.questions_phase_started_at is not None:
            self.questions_phase_started({
                "type": "questions_phase_started",
                "remaining_time": self.current_round.get_questions_phase_remaining_time()
            })
            
            return
        
    def questions_phase_started(self, event):
        if self.already_submited_question():
            return
    
        self.send(text_data=json.dumps({
            "type": event["type"],
            "remaining_time": self.current_round.get_questions_phase_remaining_time()
        }))
    
    def submit_question(self, question):
        self.current_round.refresh_from_db()
        if self.current_round.questions_phase_started_at is None:
            return
            
        if self.current_round.get_questions_phase_remaining_time() <= 0:
            return
        
        if self.already_submited_question():
            return
        
        if len(question) == 0:
            return
        
        Question(
            text=question[:128],
            author=self.player,
            round=self.current_round,
        ).save()
    
    def already_submited_question(self):
        return self.current_round.question_set.filter(author=self.player).exists()
    
    def answers_phase_started(self, event):
        if self.already_answered():
            return

        self.refresh_current_round()
        question = self.get_assigned_question()
        self.send(text_data=json.dumps({
            "type": event["type"],
            "remaining_time": self.current_round.get_answers_phase_remaining_time(),
            "question": question.text
        }))
        
    def get_assigned_question(self):
        return self.current_round.question_set.filter(respondent=self.player).first()
    
    def submit_answer(self, answer):
        if self.current_round.answers_phase_started_at is None:
            return
        
        if self.current_round.get_answers_phase_remaining_time() <= 0:
            return
        
        if self.already_answered():
            return
    
        if len(answer) == 0:
            return
        
        Answer(
            text=answer[:128],
            player=self.player,
            question=self.get_assigned_question()
        ).save()
    
    def already_answered(self):
        return self.current_round.question_set.filter(answer__player=self.player).exists()
    
    def vote_phase_started(self, event):
        self.refresh_current_round()
        self.send(text_data=json.dumps({
            "type": event["type"],
            "remaining_time": self.current_round.get_vote_phase_remaining_time(),
            "answered_questions": self.get_vote_questions()
        }))
    
    def get_vote_questions(self):
        questions = (
            Question.objects
            .select_related("answer")
            .prefetch_related("answer__vote_set")
            .filter(~Q(respondent=self.player), ~Q(author=self.player), round=self.current_round)
            .all()
        )    
        
        vote_questions = []
        for question in questions:
            vote_questions.append({
                "question": question.text,
                "answer": question.answer.text,
                "answer_id": question.answer.pk,
                "voted": question.answer.vote_set.filter(player=self.player).exists()
            })

        return vote_questions
    
    def submit_vote(self, answerId):
        Vote.objects.filter(answer__question__round=self.current_round, player=self.player).delete()
        
        Vote(
            answer_id=answerId,
            player=self.player
        ).save()
    
    def round_ended(self, event):
        self.update_current_round()
        self.send(text_data=json.dumps({
            "type": event["type"],
            "round_graphic": event["round_graphic"],
            "overall_graphic": event["overall_graphic"]
        }))
    
    def refresh_current_round(self):
        self.current_round.refresh_from_db()
    
    def update_current_round(self):
        self.room.refresh_from_db()
        self.current_round = self.room.get_current_round()
        
    def game_ended(self, event):
        self.send(text_data=json.dumps({
            "type": event["type"],
            "winner": event["winner"]
        }))   