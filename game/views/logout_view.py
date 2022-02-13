from django.http import HttpRequest
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


def logout(request: HttpRequest):
    auth_logout(request)

    return redirect('/')