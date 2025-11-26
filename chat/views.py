from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from chat.models import MessengerChannel
# Create your views here.

# @login_required
def chat_room(request, channel_id):
    context = {
        'channel_id': channel_id,
    }

    return render(request, 'chat/chat_room.html', context)
