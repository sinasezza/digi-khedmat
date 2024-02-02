from django.contrib import admin
from django.urls import path, re_path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main_view,name='main-page'),
    path('auth/',include('accounts.urls')),
    path('tahator/',include('barters.urls')),
    path('ads/', include('ads.urls')),
    path('jobs/', include('jobs.urls')),
    path('chat/', include('chat.urls')),
    
    # third party packages urls
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^watchman/', include('watchman.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

handler404 = 'generics.views.handler404'
handler500 = 'generics.views.handler500'