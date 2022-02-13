import uuid
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import is_valid_path

from game.forms.create_room_form import CreateRoomForm
from game.models.room import Room


def create_room(request: HttpRequest):

    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room: Room = form.save(commit=False)
            room.players.append(request.user)
            room.save()

            return redirect(f'/room/{room.code}')
        else:
            return render(request, 'create_room.html', {'errors': form.errors.items(), 'code': request.POST.code})

    return render(request, 'create_room.html', {'code': uuid.uuid4().hex[:6].upper()})