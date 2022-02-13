from attr import field, fields
from django import forms

from ..models import Room

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['code', 'secret']