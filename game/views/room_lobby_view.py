from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from game.guards import exact_room_guard, game_not_started_guard, has_room_guard


from ..models import Room, Player

@login_required
@has_room_guard
@exact_room_guard
@game_not_started_guard
def room_lobby(request: HttpRequest, room_code):
    room : Room = Room.objects.select_related('owner').get(code=room_code)
    return render(request, 'room_lobby.html', {'room': room})