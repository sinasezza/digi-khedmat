import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from accounts.models import Account
from . import models


def get_or_create_chat_room_view(request: HttpRequest, receiver_id: str) -> HttpResponseRedirect:
    try:
        receiver = Account.objects.get(id=receiver_id)
    except:
        return  render(request, 'common/404.html')
    
    threads = models.Thread.objects.filter((Q(user1=request.user) &  Q(user2=receiver)) | (Q(user1=receiver) & Q(user2=request.user)))
    if threads.exists():
        thread = threads.first()
    else:
        thread = models.Thread.objects.create(user1=request.user, user2=receiver)
    
        
    return redirect(thread.get_room_url())
    
# --------------------------------------------------------------

@login_required(login_url='accounts:login')
def chat_room_view(request: HttpRequest, room_name: str) -> HttpResponse:
    # Retrieve the thread or return a 404 response
    thread = get_object_or_404(models.Thread, name=room_name)
    
    sender = request.user
    receiver = thread.user1 if thread.user2 == sender else thread.user2

    # Retrieve room messages ordered by created_at
    room_messages = thread.messages.all().order_by('created_at')

    # # Send chat room information to the WebSocket
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_add)(
    #     f'group__{room_name}',
    #     {
    #         'type': 'chat.room_info',
    #         'room_name': room_name,
    #         'room_name': str(thread),
    #         'room_messages': [{'content': message.content, 'from_user': message.from_user.username} for message in room_messages],
    #     }
    # )

    context = {
        'room_name': thread.name,
        'room_messages': room_messages,
        'sender': sender,
        'receiver': receiver,
    }
    return render(request, 'chat/chat-room.html', context)
