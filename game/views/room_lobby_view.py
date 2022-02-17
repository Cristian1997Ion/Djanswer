from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from game.guards import exact_room_guard, game_not_started_guard


from ..models import Room

@login_required
@exact_room_guard
@game_not_started_guard
def room_lobby(request: HttpRequest, room_code):
    room : Room = Room.objects.select_related('owner').prefetch_related('players').get(code=room_code)
    if request.user == room.owner:
        socketUrl = f'ws://{request.get_host()}/ws/room/{room.code}/lobby/owner'
    else:
        socketUrl = f'ws://{request.get_host()}/ws/room/{room.code}/lobby'

    return render(request, 'room_lobby.html', {'players': room.players.all(), 'room': room, 'socketUrl': socketUrl})