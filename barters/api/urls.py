from django.urls import path
from . import apis

app_name = "barters-api"

urlpatterns = [
    path('barter-delete/<str:barter_slug>/', apis.barter_delete_api, name='barter-delete'),
    path('barter-delete-image/<int:id>/', apis.barter_image_delete_api, name='barter-delete-image'),
    path('barter-fetch-views/<str:barter_slug>/', apis.barter_fetch_views_api, name='barter-fetch-views'),
]
