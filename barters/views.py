import uuid
import logging
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views import generic
from . import models, forms


logger = logging.getLogger("barters.views")

def barter_list_view(request):
    barters = models.BarterAdvertising.objects.filter(status='published')
    
    logger.info(f"barter list fetched by  user {request.user}")
        
    context = {
        'barters': barters,
    }
    return render(request, 'barters/barter-list.html', context)

# ---------------------------------------------------------

# class BarterListView(generic.ListView):
#     model = models.BarterAdvertising
#     queryset = models.BarterAdvertising.objects.filter(status='published')
#     template_name = "barters/barter-list.html"
#     context_object_name = 'barters'

# ---------------------------------------------------------

def barter_detail_view(request: HttpRequest, barter_id: str, barter_slug: str):
    logger.info(f"user {request.user} requested for barter detail")
    try:
        barter = models.BarterAdvertising.objects.get(id=barter_id)
        if barter.status == 'draft':
            return render(request, 'common/404.html', status=404)
    except:
        return render(request, 'common/404.html', status=404)

    logger.info(f"user {request.user} retrieved barter detail {barter}")
    
    context = {
        'barter': barter,
    }
    return render (request, 'barters/barter-detail.html', context)

    
# ---------------------------------------------------------

def barter_update_view(request: HttpRequest, barter_id: str, barter_slug: str):
    try:
        barter = models.BarterAdvertising.objects.get(id=barter_id)
    except:
        return render(request, 'common/404.html', status=404)
    
    if not barter.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    context = {
        
    }
    
    return render(request, 'barters/barter-update.html', context)

# ---------------------------------------------------------

def barter_delete_view(request: HttpRequest, barter_id: str, barter_slug: str):
    barter = models.BarterAdvertising.objects.get(id=barter_id)
    
    if not barter.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    barter.delete()
    
    return reverse_lazy("barters:barter-list")
    
# ---------------------------------------------------------