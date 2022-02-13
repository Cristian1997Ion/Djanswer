from unicodedata import name
from django.urls import path

from game.views.logout_view import logout

from . import views

urlpatterns = [
    path('', views.home, name="home_view"),
    path('login/', views.login, name="login_view"),
    path('register/', views.register, name='register_view'),
    path('logout', views.logout, name='logout_view')
]