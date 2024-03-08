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
from generics import models as generics_models
from . import models, forms, decorators


@decorators.log_before_after
def advertise_list_view(request):
    ads = models.StuffAdvertising.objects.filter(status='published').order_by('date_published')
    
    # response to search advertise
    search_input = request.GET.get('search-area') or ''
    if search_input:
        ads = ads.filter(
            Q(title__icontains=search_input) | 
            Q(summary__icontains=search_input) | 
            Q(description__icontains=search_input) |
            Q(stuff_status__icontains=search_input) |
            Q(categories__title__icontains=search_input) |  
            Q(tags__name__icontains=search_input) |  
            Q(region__state__icontains=search_input) |  
            Q(region__city__icontains=search_input)   
        ).distinct().order_by('-date_published')
    
    # Pagination
    paginated = Paginator(ads, 8) 
    page_number = request.GET.get("page")  
    paginated_ads = paginated.get_page(page_number)
        
    context = {
        'ads': paginated_ads,
        'search_input': search_input,
    }
    return render(request, 'ads/adv-list.html', context)

# ---------------------------------------------------------

@decorators.log_before_after
def advertise_detail_view(request: HttpRequest, adv_slug: str):
    advertise = get_object_or_404(models.StuffAdvertising, slug=adv_slug, status='published')
    advertise.increment_views()
    
    # check if user added this advertising to his favorites
    try:
        favorite = request.user.favorites.get(object_id=advertise.id) 
    except:
        favorite = None
        
    context = {
        'advertise': advertise,
        'favorite': favorite,
    }
    return render (request, 'ads/adv-detail.html', context)

    
# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.log_before_after
def advertise_create_view(request):
    if request.method == 'POST':
        form = forms.StuffAdvertisingForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_adv = form.save()
            new_adv.owner = request.user
            new_adv.save()
            
            # update tags and categories
            tags = request.POST.getlist('tags')
            new_adv.update_tags(tags)

            # update categories
            cats = request.POST.getlist('categories')
            new_adv.update_categories(cats)
            
            messages.success(request, 'آگهی تبلیغاتی شما ایجاد شد.')
            return redirect('ads:attach-images', adv_slug=new_adv.slug)
    else:
        form = forms.StuffAdvertisingForm()
    
    stuff_statuses = models.StuffAdvertising.STUFF_STATUSES
    categories = generics_models.StuffCategory.objects.all()
    tags = generics_models.Tag.objects.all()
    regions = generics_models.Region.objects.all()
    
    context = {
        'form': form,
        'stuff_statuses': stuff_statuses,
        'categories': categories,
        'tags': tags,
        'regions': regions,
    }
    return render(request, 'ads/adv-create.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
@decorators.log_before_after
def advertise_image_create_view(request: HttpRequest, adv_slug: str) -> HttpResponse:
    """Add an image to existing ad."""
    advertise = get_object_or_404(models.StuffAdvertising, slug=adv_slug)
    
    if request.method == 'POST':
        images = request.FILES.getlist("images")
        if len(images) < 1:
            messages.success(request, "آگهی شما با موفقیت ساخته شد")
            return redirect('accounts:user-panel')
        
        for image in images: 
            image_obj = models.StuffImage.objects.create(stuff_advertising=advertise, image=image)
        return redirect('ads:attach-images',  adv_slug=advertise.slug)
    
    advertise_images = advertise.images.all()
    
    context = {
        'advertise': advertise,
        'advertise_images': advertise_images,
    }
    
    return render(request, 'ads/adv-attach-images.html', context)
        

# ---------------------------------------------------------


@login_required(login_url='accounts:login')
@decorators.owner_required
@decorators.log_before_after
def advertise_update_view(request: HttpRequest, adv_slug: str):
    advertise = get_object_or_404(models.StuffAdvertising, slug=adv_slug)
    
    # Get existing images related to the advertising
    existing_images = advertise.images.all()
    
    if request.method == "POST":
        form = forms.StuffAdvertisingForm(request.POST, request.FILES, instance=advertise)
        
        if form.is_valid():
            updated_advertise = form.save()
            
            # update tags and categories
            tags = request.POST.getlist('tags')
            updated_advertise.update_tags(tags)

            # update categories
            cats = request.POST.getlist('categories')
            updated_advertise.update_categories(cats)
             
            messages.success(request, 'آگهی تبلیغاتی شما به‌روزرسانی شد.')
            return redirect('ads:attach-images',  adv_slug=updated_advertise.slug)
        else:
            # print(f"error : {form.errors.as_data()}")
            messages.warning(request, "لطفا فرم را به طور صحیح پر کنید.")
            form = forms.StuffAdvertisingForm(request.POST, instance=advertise)
    else:
        form = forms.StuffAdvertisingForm(instance=advertise)
        
        
    stuff_statuses = models.StuffAdvertising.STUFF_STATUSES
    categories = generics_models.StuffCategory.objects.all()
    tags = generics_models.Tag.objects.all()
    regions = generics_models.Region.objects.all()
    
    context = {
        'advertise': advertise,
        'form': form,
        'stuff_statuses': stuff_statuses,
        'categories': categories,
        'tags': tags,
        'regions': regions,
    }
    
    return render(request, 'ads/adv-update.html', context)



# ---------------------------------------------------------