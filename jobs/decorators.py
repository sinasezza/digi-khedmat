import logging
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from . import models


logger = logging.getLogger('jobs')

def log_before_after(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Log before accessing the view
        logger.info(f"user {request.user} accessed to : {func.__name__}")
        
        # Call the view function
        result = func(request, *args, **kwargs)
        
        # Log after accessing the view
        # logger.info(f"After accessing view: {func.__name__}")
        
        return result
    return wrapper

# ---------------------------------------------------------------------

def owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        job_slug = kwargs.get('job_slug')
        job = get_object_or_404(models.JobAdvertising, slug=job_slug)
                
        # Check if the user is a owner of the job
        if request.user != job.owner:
            return redirect('generics:forbidden')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

# ---------------------------------------------------------------------

def resume_connection_required(view_func):
    """Decorator for views that checks if there's an active connection between  
       applicant and job advertisement."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

# ---------------------------------------------------------------------

def resume_owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view