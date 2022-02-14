from django.http import HttpRequest
from django.shortcuts import redirect, render
from game.guards import no_room_guard
from django.contrib.auth.decorators import login_required
from ..models import Room, Player


@login_required
@no_room_guard
def join_room(request: HttpRequest):
    player: 'Player' = request.user
    if request.method == 'POST':
        try:
            room: Room = Room.objects.get(code=request.POST.get('code', ''), secret=request.POST.get('secret', ''))
        except Room.DoesNotExist:
            return render(request, 'join_room.html', {'errors': ['Invalid room code or secret.'], 'code': request.POST.get('code')})
        
        if room.players.count() >= Room.MAX_PLAYERS:
            return render(request, 'join_room.html', {'errors': ['This room is full.'], 'code': request.POST.get('code')})

        player.join_room(room)
        return redirect('room_lobby', room_code=room.code)

    return render(request, 'join_room.html')
