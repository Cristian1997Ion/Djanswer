from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from game.guards import exact_room_guard


from ..models import Player, Room

@login_required
@exact_room_guard
def room_lobby(request: HttpRequest, room_code):
    player: Player = request.user
    if player.room and player.room.code != room_code:
        return redirect(f'/room/{player.room.code}/')
    elif not player.room:
        try:
            room: Room = Room.objects.get(code=room_code)
        except Room.DoesNotExist:
            raise Http404

        player.join_room(room)

    return HttpResponse('test')
