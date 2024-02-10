from django.urls import path
from . import views


app_name = "accounts_api"


urlpatterns = [
    path('delete-notification/<str:id>/', views.delete_notification_api, name='delete-notification'),
    path('notification-mark-as-read/<str:id>/',  views.mark_as_read_api, name='notification-mark-as-read'),
    path('add-favorite/', views.add_favorite_api, name='add-favorite'),
    path('delete-favorite/<str:id>/', views.delete_favorite_api, name='delete-favorite'),
]
