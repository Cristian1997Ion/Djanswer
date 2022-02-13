from django.http import HttpRequest
from django.shortcuts import redirect, render
from Djanswer.containers import Container
from Djanswer.services.mail_service import Mailer
from game.forms.register_form import RegisterForm
from ..models import Player
from dependency_injector.wiring import inject, Provide

@inject
def register(request: HttpRequest, mailer: Mailer = Provide[Container.mailer]):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            player: Player = registerForm.save(commit=False)
            player.set_password(player.password)
            player.save()

            # Firewall smtp timeout on my machine...
            #mailer.send([player.email], 'Welcome to Djanswer!', f'Hi, {player.username}! You can now start playing Djanswer!')

            return redirect('/login')
        else:
            print(registerForm.errors)
            return render(request, 'register.html', {'errors': registerForm.errors.items()})

    return render(request, 'register.html')
