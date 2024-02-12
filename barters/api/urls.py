from django.urls import path
from . import apis

app_name = "barters-api"

urlpatterns = [
    path('delete-barter-image/<int:id>/', apis.delete_barter_image_api, name='delete-barter-image'),
]
