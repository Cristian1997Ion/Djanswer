from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Player, Question, Vote
    from django.db.models.manager import RelatedManager

class Answer(models.Model):
    text = models.CharField(max_length=128, null=True, default=None)
    
    question: 'Question' = models.OneToOneField(to='Question', on_delete=models.CASCADE, related_name='answer')
    player: 'Player' = models.ForeignKey(to='Player', on_delete=models.DO_NOTHING)
    
    vote_set: 'RelatedManager[Vote]'
    
