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
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            player: Player = register_form.save(commit=False)
            player.set_password(player.password)
            player.save()

            # Firewall smtp timeout on my machine...
            #mailer.send([player.email], 'Welcome to Djanswer!', f'Hi, {player.username}! You can now start playing Djanswer!')

            return redirect('/login')
        else:
            print(register_form.errors)
            return render(request, 'register.html', {'errors': register_form.errors.items()})

    return render(request, 'register.html')
