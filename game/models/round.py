from typing import TYPE_CHECKING
from django.db import models
if TYPE_CHECKING:
    from . import Question, Room
    from django.db.models.manager import RelatedManager


class Round(models.Model):
    questions_phase_ended = models.BooleanField(default=False)
    answers_phase_ended = models.BooleanField(default=False)
    vote_phase_ended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, default=None)
    
    room = models.ForeignKey(to='Room', on_delete=models.CASCADE)
    
    @property
    def questions(self) -> 'RelatedManager[Question]':
        return self.question_set
    
    def fetch_current_room_round(room_id) -> 'Round':
        return Round.objects.order_by('id').filter(room_id=room_id).first()