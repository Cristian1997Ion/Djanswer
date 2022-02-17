import uuid
from django.http import HttpRequest
from django.shortcuts import redirect, render
from game.forms.create_room_form import CreateRoomForm
from game.guards import no_room_guard
from django.contrib.auth.decorators import login_required
from django.db import transaction

from ..models import Room, Player, Round


@login_required
@no_room_guard
def create_room(request: HttpRequest):
    player: 'Player' = request.user
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            with transaction.atomic():    
                room: Room = form.save(commit=False)
                room.owner = player
                room.save()
                player.join_room(room)
                Round.objects.bulk_create([Round(room=room) for _ in range(Room.ROUNDS_NUMBER)])
            return redirect('room_lobby', room_code=room.code)
        else:
            return render(request, 'create_room.html', {'errors': form.errors.items(), 'code': request.POST.get('code')})

    return render(request, 'create_room.html', {'code': uuid.uuid4().hex[:6].upper()})