from unicodedata import name
from django.db import models
from django.core.validators import RegexValidator

class Room(models.Model):
    name = models.CharField(max_length=16)
    secret = models.CharField(max_length=4, validators=[RegexValidator(r'^[0-9+]', 'Only digit characters.')])