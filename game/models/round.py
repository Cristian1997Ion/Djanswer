import datetime
from django.utils.timezone import utc
from typing import TYPE_CHECKING
from django.db import models

from game.utils import get_remaining_time
if TYPE_CHECKING:
    from . import Question, Room
    from django.db.models.manager import RelatedManager


class Round(models.Model):
    QUESTIONS_PHASE_DURATION = 30
    ANSWERS_PHASE_DURATION = 30
    VOTE_PHASE_DURATION = 30
    
    questions_phase_started_at = models.DateTimeField(default=None, null=True)
    answers_phase_started_at = models.DateTimeField(default=None, null=True)
    vote_phase_started_at = models.DateTimeField(default=None, null=True)
    ended = models.BooleanField(default=False)
    
    room: 'Room' = models.ForeignKey(to='Room', on_delete=models.CASCADE)
    question_set: 'RelatedManager[Question]'
    
    def get_questions_phase_remaining_time(self):
        if not self.questions_phase_started_at:
            return self.QUESTIONS_PHASE_DURATION

        return get_remaining_time(self.questions_phase_started_at + datetime.timedelta(seconds=self.QUESTIONS_PHASE_DURATION))
    
    def get_answers_phase_remaining_time(self):
        if not self.questions_phase_started_at:
            return self.QUESTIONS_PHASE_DURATION

        return get_remaining_time(self.answers_phase_started_at + datetime.timedelta(seconds=self.ANSWERS_PHASE_DURATION))
    
    def get_vote_phase_remaining_time(self):
        if not self.vote_phase_started_at:
            return self.vote_phase_started_at

        return get_remaining_time(self.vote_phase_started_at + datetime.timedelta(seconds=self.VOTE_PHASE_DURATION))