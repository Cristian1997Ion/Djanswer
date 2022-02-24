from time import time
from django.db import models
from django.utils.timezone import now
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Player, Answer

class Vote(models.Model):
    created_at = models.DateTimeField(default=now)
    
    player: 'Player' = models.ForeignKey(to='Player', on_delete=models.DO_NOTHING)
    answer: 'Answer' = models.ForeignKey(to='Answer', on_delete=models.CASCADE)
