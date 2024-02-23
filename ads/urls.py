from django.urls import path
from . import views

app_name = 'ads'


urlpatterns = [
    path('list/', views.advertise_list_view, name='adv-list'),
    path('detail/<str:adv_slug>/', views.advertise_detail_view, name='adv-detail'),
    path('create/', views.advertise_create_view, name='adv-create'),
    path('attach-images/<str:adv_slug>/', views.advertise_image_create_view, name='attach-images'),
    path('update/<str:adv_slug>/', views.advertise_update_view, name='adv-update'),
]