from django.urls import path
from . import views

urlpatterns = [
    path('<int:channel_id>/', views.chat_room, name='chat_room'),
]