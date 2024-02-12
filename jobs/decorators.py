from django.shortcuts import render, redirect, get_object_or_404
from . import models

def owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        job_slug = kwargs.get('job_slug')
        job = get_object_or_404(models.JobAdvertising, slug=job_slug)
                
        # Check if the user is a owner of the job
        if request.user != job.owner:
            return redirect('generics:not-found')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
