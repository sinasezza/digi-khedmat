from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register-info/', views.register_info_view, name='register-info'),
    path('login/', views.login_view, name='login'),
    path('login-otp/', views.login_otp_view, name='login-otp'),
    path('logout/',views.logout_view,name='logout'),
    path('user-panel/', views.user_panel_view, name='user-panel'),
    path('my-profile/', views.my_profile_view, name='my-profile'),
    path('user-profile/<str:id>/', views.user_profile_view, name='user-profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('favorites/', views.favorites_view, name='favorites'),
]