from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('generics.urls', namespace='generics')),
    path('auth/',include('accounts.urls', namespace='accounts')),
    path('tahator/',include('barters.urls', namespace='barters')),
    path('ads/', include('ads.urls', namespace='ads')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('chat/', include('chat.urls', namespace='chat')),
    
    # third party packages urls
    # path("__reload__/", include("django_browser_reload.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^watchman/', include('watchman.urls')),
    re_path(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

handler404 = 'generics.views.handler404'
handler500 = 'generics.views.handler500'