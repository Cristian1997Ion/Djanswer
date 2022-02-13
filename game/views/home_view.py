from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


@login_required
def home(request: HttpRequest):
    # print(request.user.is_authenticated)
    # if not request.user.is_authenticated:
    #     return redirect('/login')

    return render(request, 'home.html')

