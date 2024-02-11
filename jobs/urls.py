from django.urls import path
from . import views

app_name = 'jobs'


urlpatterns = [
    path('list/', views.JobAdvertisingListView.as_view(), name='job-list'),
    path('detail/<str:job_slug>/', views.JobAdvertisingDetailView.as_view(), name='job-detail'), 
]