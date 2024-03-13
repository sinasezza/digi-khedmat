from django.urls import path
from . import apis


app_name = "accounts_api"


urlpatterns = [
    path('delete-notification/<str:id>/', apis.delete_notification_api, name='delete-notification'),
    path('notification-mark-as-read/<str:id>/',  apis.mark_as_read_api, name='notification-mark-as-read'),
    path('add-favorite/', apis.add_favorite_api, name='add-favorite'),
    path('delete-favorite/<str:id>/', apis.delete_favorite_api, name='delete-favorite'),
    path('send-otp/', apis.send_otp_api, name='send-otp'),
    path('check-field-existence/', apis.check_field_existence_api, name='check-field-existence'),
    path('get-sidebar-counts/', apis.get_sidebar_counts_api, name='get-sidebar-counts'),
    path('get-user-ads-count/<str:username>/', apis.get_user_ads_count_api, name='get-user-ads-count'),
]
