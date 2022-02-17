import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.validators import MinLengthValidator, RegexValidator

from game.models.room import Room

# Players are temporary, only for rooms
class Player(AbstractBaseUser):
    
    email = models.EmailField()
    username = models.CharField(max_length=16, unique=True, validators=[
        RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.'),
        RegexValidator(r'^.*[a-zA-Z]+.*$', 'At least one letter must pe present.'),
        RegexValidator(r'^[a-zA-Z]+.*$', 'The first character must be a letter.')
    ])
    password = models.CharField(max_length=128, validators=[
        MinLengthValidator(6),
        RegexValidator(r'^.*[a-z]+.*$', 'At least one lowercase letter must be present.'),
        RegexValidator(r'^.*[A-Z]+.*$', 'At least one uppercase letter must be present.'),
        RegexValidator(r'^.*[0-9]+.*$', 'At least one digit must pe present.')
    ])

    room: Room = models.ForeignKey(Room, related_name='players', on_delete=models.DO_NOTHING, null=True, blank=False, default=None)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    def join_room(self, room: Room):
        if not self.room is None:
            raise Exception('Player is already in a room!')

        self.room = room
        self.save()
    
    def leave_room(self):
        if self.room is None:
            return
        
        self.room = None
        self.save()