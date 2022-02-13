from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect

from ..models import Player, Room

def room_lobby(request: HttpRequest, code):
    player: Player = request.user
    if player.room and player.room.code != code:
        return redirect(f'/room/{player.room.code}/')
    elif not player.room:
        try:
            room: Room = Room.objects.get(code=code)
        except Room.DoesNotExist:
            raise Http404

        player.join_room(room)

    return HttpResponse('test')
