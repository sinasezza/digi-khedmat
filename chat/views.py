import uuid
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
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
    
    return thread.get_room_url()
    
# --------------------------------------------------------------

@login_required(login_url='accounts:login')
def chat_room_view(request: HttpRequest, room_id: str) -> HttpResponse:
    try:
        thread = models.Thread.objects.get(id=room_id)
    except:
        return render(request, 'common/404.html', status=404)
    
    room_messages = models.Message.objects.get(thread=thread)

    context = {
        'room_messages': room_messages,
    }
    return render(request, 'chat/chat-room.html', context)

# --------------------------------------------------------------    