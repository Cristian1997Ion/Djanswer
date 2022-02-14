from unicodedata import name
from django.http import HttpRequest
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render


def login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password = password)
        if user is None:
            return render(request, 'login.html', {'errors': ['Invalid credentials']})
        
        auth_login(request, user)
        return redirect('home')
    
    return render(request, 'login.html')