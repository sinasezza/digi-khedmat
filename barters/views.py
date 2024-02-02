import uuid
import logging
from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
    barter.increment_views()
    
    context = {
        'barter': barter,
    }
    return render (request, 'barters/barter-detail.html', context)

    
# ---------------------------------------------------------

@login_required(login_url='accounts:login')
def barter_create_view(request: HttpRequest) -> HttpResponse:
    """View to create a new ad."""
    # If the request is not from POST method then display blank form
    form = forms.BarterForm(request.POST, request.FILES)
    
    if form.is_valid():
        new_barter = form.save(commit=False)
        new_barter.owner = request.user
        new_barter.save()
        
        return redirect('accounts:user-panel')

    context = {
        'form': form,
    }        
    
    return render(request, 'barters/barter-create.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
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

@login_required(login_url='accounts:login')
def barter_delete_view(request: HttpRequest, barter_id: str, barter_slug: str):
    barter = models.BarterAdvertising.objects.get(id=barter_id)
    
    if not barter.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    barter.delete()
    
    return reverse_lazy("barters:barter-list")
    
# ---------------------------------------------------------