from django.urls import path
from . import views

app_name = 'barters'


urlpatterns = [
    path('list/', views.barter_list_view, name='barter-list'),
    path('<str:barter_id>/detail/<str:barter_slug>/', views.barter_detail_view, name='barter-detail'),
    path('<str:barter_id>/update/<str:barter_slug>/', views.barter_update_view, name='barter-update'),
    path('<str:barter_id>/delete/<str:barter_slug>/', views.barter_delete_view, name='barter-delete'),
]
