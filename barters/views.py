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


logger = logging.getLogger("barters.views")

def barter_list_view(request):
    barters = models.BarterAdvertising.objects.filter(status='published')
    
    logger.info(f"barter list fetched by  user {request.user}")
    
    # response to search barter
    search_input = request.GET.get('search-area') or ''
    if search_input:
        barters = barters.filter(
            Q(title__icontains=search_input) | 
            Q(summary__icontains=search_input) | 
            Q(description__icontains=search_input)
        )
    
    # Pagination
    paginated = Paginator(barters, 6) 
    page_number = request.GET.get("page")  
    paginated_barters = paginated.get_page(page_number)
        
    context = {
        'barters': paginated_barters,
        'search_input': search_input,
    }
    return render(request, 'barters/barter-list.html', context)

# ---------------------------------------------------------

# class BarterListView(generic.ListView):
#     model = models.BarterAdvertising
#     queryset = models.BarterAdvertising.objects.filter(status='published')
#     template_name = "barters/barter-list.html"
#     context_object_name = 'barters'

# ---------------------------------------------------------

def barter_detail_view(request: HttpRequest, barter_slug: str):
    logger.info(f"user {request.user} requested for barter detail")
    try:
        barter = models.BarterAdvertising.objects.get(slug=barter_slug)
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
    if request.method == 'POST':
        form = forms.BarterForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_barter = form.save(commit=False)
            new_barter.owner = request.user
            new_barter.save()
            
            return redirect('barters:attach-images', barter_slug=new_barter.slug)
    else:
        context = {
            'form': forms.BarterForm(),
        }        
    
    return render(request, 'barters/barter-create.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
def barter_image_create_view(request: HttpRequest, barter_slug: str) -> HttpResponse:
    """Add an image to existing ad."""
    barter = get_object_or_404(models.BarterAdvertising, slug=barter_slug)
    
    if request.method == 'POST':
        ok = request.POST.get('ok', None)
        if ok is not None and ok == 'True':
            messages.success(request, "آگهی شما با موفقیت ساخته شد")
            return redirect('accounts:user-panel')
        
        images = request.FILES.getlist("images")
        
        for image in images: 
            image_obj = models.BarterImage.objects.create(image=image)
            barter.images.add(image_obj)
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
@decorators.owner_required
def barter_delete_view(request: HttpRequest, barter_id: str, barter_slug: str):
    barter = models.BarterAdvertising.objects.get(id=barter_id)
    
    if not barter.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    barter.delete()
    
    return reverse_lazy("barters:barter-list")
    
# ---------------------------------------------------------