from django.http import HttpRequest
from django.shortcuts import render


def user_card(request: HttpRequest):
    return render (request, 'components/user_card.html', {
        'username': request.GET.get('username')
    })