from django.urls import path, re_path
from . import views


app_name = 'generics'


urlpatterns = [
    path('', views.main_page_view, name='main-page'),
    path('not-found/', views.handler404, name='not-found'),
    path('server-error/', views.handler500, name='server-error'),
    path('forbidden/', views.handler403, name='forbidden'),
    path('about-us/', views.about_us_view, name='about-us'),
    path('privacy&policy/', views.privacy_policy_view, name='privacy-policy'),
    path('certificates/', views.certificates_view, name='certificates'),
    path('contact-us/', views.contact_us_view, name='contact-us'),
]
