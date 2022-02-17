from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('create/room/', views.create_room, name='create_room'),
    path('join/room/', views.join_room, name='join_room'),
    path('room/<room_code>/lobby', views.room_lobby, name='room_lobby'),
    path('room/<room_code>/game', views.room_game, name='room_game'),
    path('components/user_card', views.user_card, name='user_card')
]