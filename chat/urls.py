from django.urls import path
from . import views

app_name = "chat"


urlpatterns = [
    path('<str:customer_id>/', views.chat_room_view, name='chat-room'),
]
