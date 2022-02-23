from cgitb import text
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from game.models import Player, Room, Round, player
from channels.db import database_sync_to_async
from django.db.models import Prefetch
from game.models import question
from game.models.answer import Answer
from game.models.question import Question
import game.socket_consumers.utils as socket_utils

class RoomGameConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def initialize(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = socket_utils.get_game_channel_name(self.room_code)
        self.player: Player = self.scope['user']
        self.room: Room = (
            Room.objects
            .select_related('owner')
            .prefetch_related('players', Prefetch('rounds', queryset=Round.objects.order_by('id')))
            .get(pk=self.player.room_id)
        )
        
        if self.room.code != self.room_code:
            raise Exception
        
        self.current_round = self.room.current_round

    async def connect(self):
        await self.initialize()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.determine_phase()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'question':
            try:
                await self.question_submited(data['text']); 
            except:
                await self.send(text_data=json.dumps({
                    'type': 'question_error',
                    'error': 'An error occured while submiting your question, please try again!'
                }))
            finally:
                return
        
        if data['type'] == 'answer':
            try:
                await self.answer_submited(data['text'])
            except:
                await self.send(text_data=json.dumps({
                    'type': 'answer_error',
                    'error': 'An error occured while submiting your answer, please try again!'
                }))
            finally:
                return
        
        if data['type'] == 'answer':
            try:
                await self.answer_submited(data['text'])
            except:
                await self.send(text_data=json.dumps({
                    'type': 'answer_error',
                    'error': 'An error occured while submiting your answer, please try again!'
                }))
            finally:
                return
            
        
    async def determine_phase(self):
        if self.current_round is None:
            return
        
        if self.current_round.vote_phase_started_at is not None:
            return
        
        if self.current_round.answers_phase_started_at is not None:
            if await database_sync_to_async(self.already_answered)():
                return
            
            await self.answers_phase_started({'type': 'answers_phase_started'})
            return
        
        if self.current_round.questions_phase_started_at is not None:
            if await database_sync_to_async(self.already_submited_question)():
                return
            
            await self.questions_phase_started({
                'type': 'questions_phase_started',
                'remaining_time': self.current_round.get_questions_phase_remaining_time()
            })
            
            return
        
    async def questions_phase_started(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'remaining_time': self.current_round.get_questions_phase_remaining_time()
        }))
    
    @database_sync_to_async
    def question_submited(self, question):
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
        return self.current_round.questions.filter(author=self.player).exists()
    
    async def answers_phase_started(self, event):
        question: Question = await self.get_assigned_question()
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'remaining_time': self.current_round.get_questions_phase_remaining_time(),
            'question': question.text
        }))
        
    @database_sync_to_async
    def get_assigned_question(self):
        self.current_round.refresh_from_db()
        return self.current_round.questions.filter(respondent=self.player).first()
    
    @database_sync_to_async
    def answer_submited(self, answer):
        if self.current_round.answers_phase_started_at is None:
            return
        
        if self.current_round.vote_phase_started_at is not None:
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
        return self.current_round.questions.filter(answer__player=self.player).exists()