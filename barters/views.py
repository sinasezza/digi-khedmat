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
from accounts.models import Favorite
from generics import models as generics_models
from . import models, forms, decorators


@decorators.log_before_after
def barter_list_view(request):
    barters = models.BarterAdvertising.objects.filter(status='published').order_by('-date_published')
    
    # search barter advertising based on search input
    search_input = request.GET.get('search-area') or ''
    if search_input:
        barters = barters.filter(
            Q(title__icontains=search_input) | 
            Q(summary__icontains=search_input) | 
            Q(description__icontains=search_input) |
            Q(categories__title__icontains=search_input) |  
            Q(tags__name__icontains=search_input) |  
            Q(region__state__icontains=search_input) |  
            Q(region__city__icontains=search_input)   
        ).distinct().order_by('-date_published')
    
    # paginate advertising items
    paginated = Paginator(barters, 8) 
    page_number = request.GET.get("page")  
    paginated_barters = paginated.get_page(page_number)
        
    context = {
        'barters': paginated_barters,
        'search_input': search_input,
    }
    return render(request, 'barters/barter-list.html', context)

# ---------------------------------------------------------

@decorators.log_before_after
def barter_detail_view(request: HttpRequest, barter_slug: str):
    barter = get_object_or_404(models.BarterAdvertising, slug=barter_slug, status='published')
    barter.increment_views()
    
    # check if user added this advertising to his favorites
    try:
        favorite = request.user.favorites.get(object_id=barter.id) 
    except:
        favorite = None

    context = {
        'barter': barter,
        'favorite': favorite,
    }
    return render (request, 'barters/barter-detail.html', context)

    
# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.log_before_after
def barter_create_view(request: HttpRequest) -> HttpResponse:
    """View to create a new barter advertisement."""
    if request.method == 'POST':
        # If the request is POST, process the form data
        form = forms.BarterForm(request.POST)

        if form.is_valid():
            new_barter = form.save(commit=False)
            new_barter.owner = request.user
            new_barter.save()
            
            # update tags
            tags = request.POST.getlist('tags')
            new_barter.update_tags(tags)

            # update categories
            cats = request.POST.getlist('categories')
            new_barter.update_categories(cats)

            messages.success(request, f"آگهی شما ثبت شد.")

            return redirect('barters:attach-images', new_barter.slug)
        else:
            messages.error(request, "مشکلی در ثبت آگهی پیش آمده، دوباره تلاش کنید.")
            print(f"form : error : {form.errors.as_data()}")
    else:
        form = forms.BarterForm()

    regions = generics_models.Region.objects.all()
    categories = generics_models.StuffCategory.objects.all()
    tags = generics_models.Tag.objects.all()
    
    context = {
        'form': form,
        'regions': regions,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'barters/barter-create.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
@decorators.log_before_after
def barter_image_create_view(request: HttpRequest, barter_slug: str) -> HttpResponse:
    """Add an image to existing ad."""
    barter = get_object_or_404(models.BarterAdvertising, slug=barter_slug)
    
    if request.method == 'POST':
        images = request.FILES.getlist("images")
        if len(images) < 1:
            messages.success(request, "آگهی شما با موفقیت ساخته شد")
            return redirect('accounts:user-panel')
        
        for image in images: 
            image_obj = models.BarterImage.objects.create(barter_advertising=barter, image=image)
        return redirect('barters:attach-images',  barter_slug=barter.slug)
    
    barter_images = barter.images.all()
    
    context = {
        'barter': barter,
        'barter_images': barter_images,
    }
    
    return render(request, 'barters/attach-images.html', context)
        

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
@decorators.log_before_after
def barter_update_view(request: HttpRequest, barter_slug: str):
    barter = get_object_or_404(models.BarterAdvertising, slug=barter_slug)
    
    if request.method == "POST":
        form = forms.BarterForm(request.POST, request.FILES, instance=barter)
        if form.is_valid():
            updated_barter = form.save()
            
            # update tags and categories
            tags = request.POST.getlist('tags')
            updated_barter.update_tags(tags)

            # update categories
            cats = request.POST.getlist('categories')
            updated_barter.update_categories(cats)
            
            return redirect('barters:attach-images', barter_slug=updated_barter.slug)
    else:
        form = forms.BarterForm(instance=barter) 
        
    regions = generics_models.Region.objects.all()
    categories = generics_models.StuffCategory.objects.all()
    tags = generics_models.Tag.objects.all()
        
    context = {
        'form': form,
        'regions': regions,
        'categories': categories,
        'tags': tags,
        'barter': barter,
    }
    
    return render(request, 'barters/barter-update.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
@decorators.log_before_after
def barter_delete_view(request: HttpRequest, barter_id: str, barter_slug: str):
    barter = get_object_or_404(models.BarterAdvertising, slug=barter_slug)
    
    if request.method == "POST":
        barter.delete()
        messages.success(request, f"{barter} has been deleted.")
        return reverse_lazy("barters:barter-list")
    
# ---------------------------------------------------------