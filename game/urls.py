from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home_view"),
    path('login/', views.login, name="login_view"),
    path('register/', views.register, name='register_view'),
    path('logout', views.logout, name='logout_view'),
    path('create/room/', views.create_room, name='create_room_view'),
    path('room/<room_code>/', views.room_lobby, name='room_lobby'),
    path('join/room/', views.join_room, name='join_room_view'),
]