from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from game.guards import exact_room_guard


from ..models import Player, Room

@login_required
@exact_room_guard
def room_lobby(request: HttpRequest, room_code):
    return HttpResponse('test')
