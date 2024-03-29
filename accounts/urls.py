from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register-info/', views.register_info_view, name='register-info'),
    path('login/', views.login_view, name='login'),
    path('activate-account/', views.activate_account_view, name='activate-account'),
    path('logout/',views.logout_view,name='logout'),
    path('delete-account/', views.delete_account_view, name='delete-account'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('user-panel/', views.user_panel_view, name='user-panel'),
    path('my-profile/', views.my_profile_view, name='my-profile'),
    path('user-profile/@<str:username>/', views.user_profile_view, name='user-profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('favorites/', views.favorites_view, name='favorites'),
]