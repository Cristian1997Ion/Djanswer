from django.http import HttpRequest
from django.shortcuts import redirect, render


def home(request: HttpRequest):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'home.html')

