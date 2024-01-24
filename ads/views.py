from django.shortcuts import render
from django.views import generic
from . import models, forms


class AdvertiseListView(generic.ListView):
    model = models.Advertise
    queryset = models.Advertise.objects.filter(status='published')
    template_name = "ads/adv-list.html"
    context_object_name = 'ads'

# ---------------------------------------------------------

class AdvertiseDetailView(generic.ListView):
    model = models.Advertise
    queryset = models.Advertise.objects.filter(status='published')
    template_name = "ads/adv-detail.html"
    context_object_name = 'adv'
    pk_url_kwarg = 'adv_id'
