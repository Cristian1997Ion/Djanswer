from typing import Final, TYPE_CHECKING
from django.db import models

from django.core.validators import RegexValidator

if TYPE_CHECKING:
    from . import Player, Round
    from django.db.models.manager import RelatedManager

class Room(models.Model):
    MAX_PLAYERS: Final = 12
    ROUNDS_NUMBER: Final = 3

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
    round_set: 'RelatedManager[Round]'
    player_set: 'RelatedManager[Player]'
    
    @property
    def current_round(self) -> 'Round|None':
        return self.round_set.filter(ended=False).order_by('id').first()