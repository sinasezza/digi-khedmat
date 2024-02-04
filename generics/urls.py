from django.urls import path, re_path
from . import views


app_name = 'generics'


urlpatterns = [
    path('', views.main_page_view, name='main-page'),
]
