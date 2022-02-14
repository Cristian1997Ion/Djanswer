from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from game.guards import exact_room_guard


from ..models import Player, Room

@login_required
@exact_room_guard
def room_lobby(request: HttpRequest, room_code):
    room : Room = Room.objects.prefetch_related('players').get(code=room_code)

    return render(request, 'room_lobby.html', {'players': room.players.all(), 'room': room})