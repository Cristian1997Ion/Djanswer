from typing import Final, TYPE_CHECKING
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.manager import BaseManager

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

    owner = models.OneToOneField(to='Player', on_delete=models.DO_NOTHING, related_name='owned_room')
    
    @property
    def players(self) -> BaseManager:
        return self.player_set
