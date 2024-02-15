from django.urls import path
from . import views

app_name = 'jobs'


urlpatterns = [
    path('list/', views.job_list_view, name='job-list'),
    path('detail/<str:job_slug>/', views.job_detail_view, name='job-detail'), 
    path('create/', views.job_create_view, name='job-create'),
    path('update/<str:job_slug>/', views.job_update_view, name='job-update'),
    # path('create-pdf/', views.write_pdf_view, name='create-pdf'),
    # path('create-pdf2/', views.write_pdf_view2, name='create-pdf2'),
    path('resume/detail/<str:id>/', views.resume_detail_view, name='resume-detail'),
]