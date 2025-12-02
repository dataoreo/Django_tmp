from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from chat.models import MessengerChannel
# Create your views here.

# @login_required
def chat_room(request, channel_id):
    context = {
        'channel_id': channel_id,
    }

    return render(request, 'chat/chat_room.html', context)