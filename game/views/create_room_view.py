import uuid
from django.http import HttpRequest
from django.shortcuts import redirect, render
from game.forms.create_room_form import CreateRoomForm
from ..models import Room, Player



def create_room(request: HttpRequest):
    player: 'Player' = request.user
    if player.room is None:
        return redirect(f'/room/{request.user.room.code}/')

    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room: Room = form.save(commit=False)
            room.save()
            player.join_room(room)

            return redirect(f'/room/{room.code}')
        else:
            return render(request, 'create_room.html', {'errors': form.errors.items(), 'code': request.POST.code})

    return render(request, 'create_room.html', {'code': uuid.uuid4().hex[:6].upper()})