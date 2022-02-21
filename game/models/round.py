import datetime
from django.utils.timezone import utc
from typing import TYPE_CHECKING
from django.db import models
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
    
    room = models.ForeignKey(to='Room', on_delete=models.CASCADE)
    
    @property
    def questions(self) -> 'RelatedManager[Question]':
        return self.question_set
    
    def get_questions_phase_remaining_time(self):
        if not self.questions_phase_started_at:
            return self.QUESTIONS_PHASE_DURATION

        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.questions_phase_started_at
        remaining_seconds = self.QUESTIONS_PHASE_DURATION - int(timediff.total_seconds())
        return remaining_seconds if remaining_seconds > 0 else 0