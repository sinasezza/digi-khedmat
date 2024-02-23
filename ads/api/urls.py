from django.urls import path
from . import apis


app_name = "ads-api"


urlpatterns = [
    path('stuff-ads-image-delete/<int:id>/', apis.stuff_image_delete_api, name='stuff-image-delete'),
]
