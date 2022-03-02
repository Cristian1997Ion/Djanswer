from django.db import models

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Player, Round, Answer

class Question(models.Model):
    text = models.CharField(max_length=128, null=True, default=None)
    
    round: 'Round' = models.ForeignKey(to='Round', on_delete=models.CASCADE)
    author: 'Player' = models.ForeignKey(to='Player', on_delete=models.DO_NOTHING, related_name='asked_questions')
    respondent: 'Player' = models.ForeignKey(to='Player', on_delete=models.DO_NOTHING, related_name='answered_questions', null=True, default=None)
    answer: 'Answer'