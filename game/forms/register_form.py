from attr import field, fields
from django import forms

from ..models import Player

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = Player
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data    = super(RegisterForm, self).clean()
        password        = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirm_password')

        if password != confirmPassword:
            self.add_error('confirm_password', 'The passwords must match')
        
        return cleaned_data