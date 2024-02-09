from django.urls import path
from . import views

app_name = "chat"


urlpatterns = [
    path('room-list/', views.room_list_view, name='room-list'),
    path('<str:room_name>/', views.chat_room_view, name='chat-room'),
    path('get-create-chat-room/<str:receiver_id>/', views.get_or_create_chat_room_view, name='get-create-chat-room'),
]
