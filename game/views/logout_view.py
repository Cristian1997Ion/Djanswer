from django.http import HttpRequest
from django.contrib.auth import logout as authLogout
from django.shortcuts import redirect


def logout(request: HttpRequest):
    authLogout(request)

    return redirect('/')