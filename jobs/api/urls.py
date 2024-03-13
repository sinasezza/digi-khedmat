from django.urls import path
from . import apis


app_name = "jobs-api"


urlpatterns = [
    path('resumes/resume-delete/<str:id>/', apis.resume_delete_api, name='resume-delete'),
    path('resumes/resume-file-delete/<str:id>/', apis.resume_file_delete_api, name='resume-file-delete'),
    path('job-fetch-views/<str:job_slug>/', apis.job_fetch_views_api, name='job-fetch-views'),
]
