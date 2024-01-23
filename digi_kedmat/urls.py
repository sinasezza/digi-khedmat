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
    
    # third party packages urls
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)