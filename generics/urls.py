from django.urls import path, re_path
from . import views


app_name = 'generics'


urlpatterns = [
    path('', views.main_page_view, name='main-page'),
    path('not-found/', views.handler404, name='not-found'),
    path('server-error/', views.handler500, name='server-error'),
]
