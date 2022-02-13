from django.http import HttpRequest
from django.shortcuts import redirect, render
from game.forms.register_form import RegisterForm
from ..models import Player

def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            player: Player = registerForm.save(commit=False)
            player.set_password(player.password)
            player.save()
            
            return redirect('/login')
        else:
            print(registerForm.errors)
            return render(request, 'register.html', {'errors': registerForm.errors.items()})

    return render(request, 'register.html')
