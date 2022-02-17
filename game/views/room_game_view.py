from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from game.guards import exact_room_guard


from ..models import Room

@login_required
@exact_room_guard
def room_game(request: HttpRequest, room_code):
    room : Room = Room.objects.prefetch_related('rounds__questions').get(code=room_code)

    return render(request, 'room_game.html', {'players': room.players.all(), 'room': room})