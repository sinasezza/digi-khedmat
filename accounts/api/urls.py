from django.urls import path
from . import apis


app_name = "accounts_api"


urlpatterns = [
    path('delete-notification/<str:id>/', apis.delete_notification_api, name='delete-notification'),
    path('notification-mark-as-read/<str:id>/',  apis.mark_as_read_api, name='notification-mark-as-read'),
    path('add-favorite/', apis.add_favorite_api, name='add-favorite'),
    path('delete-favorite/<str:id>/', apis.delete_favorite_api, name='delete-favorite'),
    path('send-otp/', apis.send_otp_api, name='send-otp'),
]
