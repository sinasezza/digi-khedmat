from django.urls import path
from . import views

app_name = "chat"


urlpatterns = [
    path('<str:room_id>/', views.chat_room_view, name='chat-room'),
    path('get-create-chat-room/', views.get_or_create_chat_room_view, name='get-create-chat-room')
]
