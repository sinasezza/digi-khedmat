from django.urls import path
from . import views

app_name = 'barter'


urlpatterns = [
    path('list/', views.stuff_list_view, name='stuff-list'),
    path('<str:stuff_id>/detail/<str:stuff_slug>/', views.stuff_detail_view, name='stuff-detail'),
    path('<str:stuff_id>/update/<str:stuff_slug>/', views.stuff_update_view, name='stuff-update'),
    path('<str:stuff_id>/delete/<str:stuff_slug>/', views.stuff_delete_view, name='stuff-delete'),
]
