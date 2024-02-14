import uuid
import logging
from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views import generic
from . import models, forms, decorators



def advertise_list_view(request):
    ads = models.Advertise.objects.filter(status='published')
    
    # logger.info(f"advertise list fetched by  user {request.user}")
    
    # response to search advertise
    search_input = request.GET.get('search-area') or ''
    if search_input:
        ads = ads.filter(
            Q(title__icontains=search_input) | 
            Q(summary__icontains=search_input) | 
            Q(description__icontains=search_input)
        )
    
    # Pagination
    paginated = Paginator(ads, 10) 
    page_number = request.GET.get("page")  
    paginated_ads = paginated.get_page(page_number)
        
    context = {
        'ads': paginated_ads,
        'search_input': search_input,
    }
    return render(request, 'ads/adv-list.html', context)

# ---------------------------------------------------------

def advertise_detail_view(request: HttpRequest, advertise_slug: str):
    advertise = get_object_or_404(models.StuffAdvertising, slug=advertise_slug, status='published')
    advertise.increment_views()
    
    context = {
        'advertise': advertise,
    }
    return render (request, 'ads/adv-detail.html', context)

    
# ---------------------------------------------------------

@login_required(login_url='accounts:login')
def advertise_create_view(request: HttpRequest) -> HttpResponse:
    
    context = {}
    return render(request, 'ads/adv-create.html', context)

# ---------------------------------------------------------


@login_required(login_url='accounts:login')
@decorators.owner_required
def advertise_update_view(request: HttpRequest, advertise_slug: str):
    advertise = get_object_or_404(models.BarterAdvertising, slug=advertise_slug)
    
    if request.method == "POST":
        form = forms.StuffAdvertisingForm(request.POST, request.FILES, instance=advertise)
        if form.is_valid():
            updated_advertise = form.save()
            return redirect('ads:attach-images', advertise_slug=updated_advertise.slug)
    else:
        form = forms.StuffAdvertisingForm(instance=advertise) 
    
    context = {
        'form': form,
    }
    
    return render(request, 'ads/adv-update.html', context)

# ---------------------------------------------------------