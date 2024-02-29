from django.urls import path
from . import apis


app_name = "jobs-api"


urlpatterns = [
    path('resumes/resume-delete/<str:id>/', apis.resume_delete_api, name='resume-delete'),
    path('resumes/resume-file-delete/<str:id>/', apis.resume_file_delete_api, name='resume-file-delete'),
]
