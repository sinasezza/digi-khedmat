from django.urls import path
from . import views

app_name = 'jobs'


urlpatterns = [
    path('list/', views.job_list_view, name='job-list'),
    path('detail/<str:job_slug>/', views.job_detail_view, name='job-detail'), 
    path('create/', views.job_create_view, name='job-create'),
    path('update/<str:job_slug>/', views.job_update_view, name='job-update'),
    path('resume/detail/<str:id>/', views.resume_detail_view, name='resume-detail'),
    path('resume-file-create/<str:job_slug>/', views.resume_file_create_view, name='resume-file-create'),
    path('resume-create/<str:job_slug>/', views.resume_create_view, name='resume-create'),
]