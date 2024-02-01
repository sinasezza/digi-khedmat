from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def chat_room_view(request: HttpRequest) -> HttpResponse:

    context = {}
    return render(request, 'chat/chat-room.html', context)