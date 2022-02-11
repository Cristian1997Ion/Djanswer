from ast import alias
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

from game.models.room import Room

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=16)