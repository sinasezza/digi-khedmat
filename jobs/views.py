import uuid
import logging
from typing import Any
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from . import models, forms, decorators


logger = logging.getLogger("jobs.views")


# ************************************** JOB ADVERTISING VIEWS **************************************


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


# ************************************** RESUME VIEWS **************************************


@login_required(login_url="accounts:login")
def  resume_upload_view(request: HttpRequest) -> HttpResponseRedirect:
    """View for uploading a user's CV."""
    if request.method == "POST":
        form = forms.ResumeUploadForm(data=request.POST, files=request.FILES or None)
        
        if not form.is_valid():
            messages.error(request, "Please correct the errors below.")
            
        else:
            # Save the file to MEDIA_ROOT directory and create Resume object with it
            pass

# ---------------------------------------------------------

def resume_detail_view(request, id):
    resume = models.Resume.objects.get(id=id)
    
    context = {
        'resume': resume,
    }
    
    return  render(request, 'jobs/resumes/resume-details.html', context)


# def write_pdf_view(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)

#     # Start writing the PDF here
#     p.drawString(100, 100, 'resume and title')
#     resume = models.Resume.objects.first()
#     p.drawString(100, 200, f"Title: {resume.title}")
#     p.drawString(100, 300, f"Author: {resume.fname}")
#     p.drawString(100, 400, f"Year: {resume.lname}")
#     # End writing

#     p.showPage()
#     p.save()

#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)

#     return response


# def write_pdf_view2(request):
#     doc = SimpleDocTemplate("/tmp/somefilename.pdf")
#     styles = getSampleStyleSheet()
#     Story = [Spacer(1,2*inch)]
#     style = styles["Normal"]
#     for i in range(100):
#        bogustext = ("This is Paragraph number %s.  " % i) * 20
#        p = Paragraph(bogustext, style)
#        Story.append(p)
#        Story.append(Spacer(1,0.2*inch))
#     doc.build(Story)

#     fs = FileSystemStorage("/tmp")
#     with fs.open("somefilename.pdf") as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#         return response

#     return response

# ---------------------------------------------------------
