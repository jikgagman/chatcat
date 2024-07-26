# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.enter_chat, name='enter_chat'),
    path('chat/', views.chat, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('remove_character/<int:user_id>/', views.remove_character, name='remove_character'),
]