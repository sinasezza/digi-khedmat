from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('user-panel/', views.user_panel_view, name='user-panel'),
    path('user-profile/', views.user_profile_view, name='user-profile'),
    path('notifications/', views.notifications_view, name='notifications'),
]