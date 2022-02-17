from typing import Final, TYPE_CHECKING
from django.db import models

from django.core.validators import RegexValidator

if TYPE_CHECKING:
    from . import Player, Round
    from django.db.models.manager import RelatedManager

class Room(models.Model):
    MAX_PLAYERS: Final = 12
    ROUNDS_NUMBER: Final = 5

    code = models.CharField(
        max_length=6,
        unique=True,
        default='error',
        error_messages={'unique': 'This code was already taken. Please try again.'},
        validators=[RegexValidator(r'^[a-zA-Z]*', 'Only alphanumerical characters.')]
    )

    secret = models.CharField(max_length=4, validators=[RegexValidator(r'^[0-9+]', 'Only digit characters.')], blank=True, default='')
    game_started = models.BooleanField(default=False)

    owner = models.OneToOneField(to='Player', on_delete=models.DO_NOTHING, related_name='owned_room')
    
    @property
    def players(self) -> 'RelatedManager[Player]':
        return self.player_set
    
    @property
    def rounds(self) -> 'RelatedManager[Round]':
        return self.round_set