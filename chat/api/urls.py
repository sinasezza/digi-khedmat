from django.urls import path
from . import apis

app_name = "chat_api"


urlpatterns = [
    path('room-delete/<str:name>/', apis.room_delete_api, name='room-delete'),
    path('room-report/<str:name>/', apis.room_report_api, name='room-report'),
]
