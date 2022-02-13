from unicodedata import name
from django.urls import path
from game.views.create_room_view import create_room

from game.views.logout_view import logout

from . import views

urlpatterns = [
    path('', views.home, name="home_view"),
    path('login/', views.login, name="login_view"),
    path('register/', views.register, name='register_view'),
    path('logout', views.logout, name='logout_view'),
    path('create/room/', views.create_room, name='create_room_view'),
    path('room/<code>/', views.room_lobby, name='room_lobby')
]