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


logger = logging.getLogger("jobs.views")

def job_list_view(request):
    jobs = models.JobAdvertising.objects.filter(status='published')
    
    logger.info(f"job list fetched by  user {request.user}")
    
    # response to search job
    search_input = request.GET.get('search-area') or ''
    if search_input:
        jobs = jobs.filter(
            Q(title__icontains=search_input) | 
            Q(summary__icontains=search_input) | 
            Q(description__icontains=search_input)
        )
    
    # Pagination
    paginated = Paginator(jobs, 6) 
    page_number = request.GET.get("page")  
    paginated_jobs = paginated.get_page(page_number)
        
    context = {
        'jobs': paginated_jobs,
        'search_input': search_input,
    }
    return render(request, 'jobs/job-list.html', context)

# ---------------------------------------------------------

def job_detail_view(request: HttpRequest, job_slug: str):
    logger.info(f"user {request.user} requested for job detail")
    job = get_object_or_404(models.JobAdvertising, slug=job_slug, status='published')
    logger.info(f"user {request.user} retrieved job detail {job}")
    
    job.increment_views()
    
    context = {
        'job': job,
    }
    return render (request, 'jobs/job-detail.html', context)

    
# ---------------------------------------------------------

@login_required(login_url='accounts:login')
def job_create_view(request: HttpRequest) -> HttpResponse:
    """View to create a new ad."""
    # If the request is not from POST method then display blank form
    if request.method == 'POST':
        form = forms.JobAdvertisingForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.owner = request.user
            new_job.save()
            
            return redirect('jobs:attach-images', job_slug=new_job.slug)
    else:
        context = {
            'form': forms.JobAdvertisingForm(),
        }        
    
    return render(request, 'jobs/job-create.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
def job_image_create_view(request: HttpRequest, job_slug: str) -> HttpResponse:
    """Add an image to existing ad."""
    job = get_object_or_404(models.JobAdvertising, slug=job_slug)
    
    if request.method == 'POST':
        ok = request.POST.get('ok', None)
        if ok is not None and ok == 'True':
            messages.success(request, "آگهی شما با موفقیت ساخته شد")
            return redirect('accounts:user-panel')
        
        images = request.FILES.getlist("images")
        
        for image in images: 
            image_obj = models.BarterImage.objects.create(image=image)
            job.images.add(image_obj)
        return redirect('jobs:attach-images',  job_slug=job.slug)
    
    job_images = job.images.all()
    
    context = {
        'job': job,
        'job_images': job_images,
    }
    
    return render(request, 'jobs/attach-images.html', context)
        

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
def job_update_view(request: HttpRequest, job_slug: str):
    job = get_object_or_404(models.JobAdvertising, slug=job_slug)
    
    if request.method == "POST":
        form = forms.JobAdvertisingForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            updated_job = form.save()
            return redirect('jobs:attach-images', job_slug=updated_job.slug)
    else:
        form = forms.JobAdvertisingForm(instance=job) 
    
    context = {
        'form': form,
    }
    
    return render(request, 'jobs/job-update.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
def job_delete_view(request: HttpRequest, job_id: str, job_slug: str):
    job = get_object_or_404(models.JobAdvertising, slug=job_slug)
    
    if request.method == "POST":
        job.delete()
        messages.success(request, f"{job} has been deleted.")
        return reverse_lazy("jobs:job-list")
    
# ---------------------------------------------------------