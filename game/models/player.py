from django.db import models
from django.contrib.auth.models import AbstractBaseUser
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

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'