from django.urls import path
from . import views

app_name = 'ads'


urlpatterns = [
    path('list/', views.AdvertiseListView.as_view(), name='adv-list'),
    path('<str:adv_id>/detail/<str:adv_slug>/', views.AdvertiseDetailView.as_view(), name='adv-detail'),
]