from django.http import HttpRequest
from django.shortcuts import redirect


def no_room_guard(function):
    """
    Checks that the user is not in a room, redirecting
    to the room lobby page if it is.
    """
    def guard(request: HttpRequest, *args, **kwargs):
        if request.user.room:
            return redirect(f'/room/{request.user.room.code}')

        return function(request, *args, **kwargs)
    return guard

def exact_room_guard(function):
    """
    Checks that the user is not in a room, redirecting
    to the room lobby page if it is.
    """
    def guard(request: HttpRequest, *args, **kwargs):
        if not request.user.room:
            return redirect('/')
        
        if request.user.room.code != kwargs['room_code']:
            return redirect(f'/room/{request.user.room.code}')

        return function(request, *args, **kwargs)
    return guard