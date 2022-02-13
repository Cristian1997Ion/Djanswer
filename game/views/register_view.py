from django.forms import ValidationError, modelform_factory
from django.http import HttpRequest
from django.shortcuts import redirect, render
from game.forms.register_form import RegisterForm
from ..models import Player

def register(request: HttpRequest):
    if request.method == 'POST':
        # email = request.POST.get('email', '')
        # username = request.POST.get('username', '')
        # password = request.POST.get('password', '')
        # confirmPassword = request.POST.get('confirmPassword', '')    

        # if not confirmPassword != password:
        #     return render(request, 'register.html', {'error': 'The passwords must match!'})

        # try:
        #     player = Player(email=email, username=username, password=password)
        #     player.full_clean()
        #     player.save()
        # except ValidationError as error:
        #     return render(request, 'register.html', {'error': error})

        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            player: Player = registerForm.save(commit=False)
            player.set_password(player.password)
            player.save()
            
            return redirect('/game')
        else:
            print(registerForm.errors)
            return render(request, 'register.html', {'errors': registerForm.errors.items()})

    return render(request, 'register.html')
