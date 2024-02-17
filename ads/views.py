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
    ads = models.StuffAdvertising.objects.filter(status='published')
    
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
def advertise_create_view(request):
    if request.method == 'POST':
        form = forms.StuffAdvertisingForm(data=request.POST, files=request.FILES)
        formset = forms.StuffImagesFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            new_adv = form.save()
            new_adv.owner = request.user
            new_adv.save()
            
            formset.instance = new_adv
            formset.save()
            messages.success(request, 'آگهی تبلیغاتی شما ایجاد شد.')
            return redirect('accounts:user-panel')
    else:
        form = forms.StuffAdvertisingForm()
        formset = forms.StuffImagesFormSet()
    
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'ads/adv-create.html', context)

# ---------------------------------------------------------


@login_required(login_url='accounts:login')
@decorators.owner_required
def advertise_update_view(request: HttpRequest, adv_slug: str):
    advertise = get_object_or_404(models.StuffAdvertising, slug=adv_slug)
    
    # Get existing images related to the advertising
    existing_images = advertise.images.all()
    
    if request.method == "POST":
        form = forms.StuffAdvertisingForm(request.POST, request.FILES, instance=advertise)
        formset = forms.StuffImagesFormSet(request.POST, request.FILES, instance=advertise)
        
        if form.is_valid() and formset.is_valid():
            updated_advertise = form.save()
            formset.save()
            
            # Process deleted images
            for form in formset.deleted_forms:
                instance = form.instance
                instance.delete()
                
            messages.success(request, 'آگهی تبلیغاتی شما به‌روزرسانی شد.')
            return redirect('accounts:user-panel')
    else:
        form = forms.StuffAdvertisingForm(instance=advertise)
        formset = forms.StuffImagesFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'existing_images': existing_images,
    }
    
    return render(request, 'ads/adv-update.html', context)



# ---------------------------------------------------------