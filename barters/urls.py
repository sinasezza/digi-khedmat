from django.urls import path
from . import views

app_name = 'barters'


urlpatterns = [
    path('list/', views.barter_list_view, name='barter-list'),
    path('detail/<str:barter_slug>/', views.barter_detail_view, name='barter-detail'),
    path('update/<str:barter_slug>/', views.barter_update_view, name='barter-update'),
    path('delete/<str:barter_slug>/', views.barter_delete_view, name='barter-delete'),
    path('create/', views.barter_create_view, name='barter-create'),
    path('create/attach-images/<str:barter_slug>/', views.barter_image_create_view, name='attach-images'),
]
