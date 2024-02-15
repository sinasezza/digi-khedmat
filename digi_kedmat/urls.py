from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    # ******************************** MVTs ********************************
    path('admin/', admin.site.urls),
    path('', include('generics.urls', namespace='generics')),
    path('auth/',include('accounts.urls', namespace='accounts')),
    path('tahator/',include('barters.urls', namespace='barters')),
    path('ads/', include('ads.urls', namespace='ads')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('chat/', include('chat.urls', namespace='chat')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/global/images/digi-khedmat-favicon.png', permanent=True)),
    
    
    # ******************************** APIs ********************************
    path('api/auth/' , include('accounts.api.urls', namespace='accounts-api')), 
    path('api/barters/', include('barters.api.urls', namespace='barters-api')),  

    
    
    # **************************** 3rd Parties *****************************
    path("__reload__/", include("django_browser_reload.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^watchman/', include('watchman.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

handler404 = 'generics.views.handler404'
handler500 = 'generics.views.handler500'
handler403 = 'generics.views.handler403'