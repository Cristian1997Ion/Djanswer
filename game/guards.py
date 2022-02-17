from django.http import HttpRequest
from django.shortcuts import redirect

from game.models import Player
from django.db import connection


def no_room_guard(function):
    """
    Checks that the user is not in a room, redirecting
    to the room lobby page if it is.
    """
    def guard(request: HttpRequest, *args, **kwargs):
        if request.user.room:
            return redirect('room_lobby', room_code=request.user.room.code)

        return function(request, *args, **kwargs)
    return game_not_started_guard(guard)

def exact_room_guard(function):
    """
    Checks that the user is not in a room, redirecting
    to the room lobby page if it is.
    """
    def guard(request: HttpRequest, *args, **kwargs):
        player: Player = request.user
        if not player.room:
            return redirect('/')
        
        if player.room.code != kwargs['room_code']:
            return redirect('room_lobby', room_code=player.room.code)

        return function(request, *args, **kwargs)
    return guard

def game_not_started_guard(function):
    """
    Checks that the user is not in a room, redirecting
    to the room lobby page if it is.
    """
    def guard(request: HttpRequest, *args, **kwargs):
        player: Player = request.user
        if player.room.game_started:
            return redirect('room_game', room_code=player.room.code)

        return function(request, *args, **kwargs)
    return guard