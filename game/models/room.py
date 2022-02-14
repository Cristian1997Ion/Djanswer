from typing import Final, List, TYPE_CHECKING, Set
from django.db import models
from django.core.validators import RegexValidator

if TYPE_CHECKING:
    from . import Player

class Room(models.Model):
    MAX_PLAYERS: Final = 12

    code = models.CharField(
        max_length=6,
        unique=True,
        default='error',
        error_messages={'unique': 'This code was already taken. Please try again.'},
        validators=[RegexValidator(r'^[a-zA-Z]*', 'Only alphanumerical characters.')]
    )

    secret = models.CharField(max_length=4, validators=[RegexValidator(r'^[0-9+]', 'Only digit characters.')], blank=True, default='')
    
    @property
    def players(self) -> Set['Player']:
        return self.player_set
