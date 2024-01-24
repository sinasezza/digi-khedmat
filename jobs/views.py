from django.shortcuts import render
from django.views import generic
from . import models, forms


class JobAdvertisingListView(generic.ListView):
    model = models.JobAdvertising
    queryset = models.JobAdvertising.objects.filter(status='published')
    template_name = "jobs/job-list.html"
    context_object_name = 'jobs'

# ---------------------------------------------------------

class JobAdvertisingDetailView(generic.ListView):
    model = models.JobAdvertising
    queryset = models.JobAdvertising.objects.filter(status='published')
    template_name = "jobs/job-detail.html"
    context_object_name = 'job'
    pk_url_kwarg = 'adv_id'
