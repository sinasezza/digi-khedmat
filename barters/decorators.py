import logging
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from . import models


logger = logging.getLogger('barters')

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

# ---------------------------------------------------------------------------

def owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        barter_slug = kwargs.get('barter_slug')
        barter = get_object_or_404(models.BarterAdvertising, slug=barter_slug)
                
        # Check if the user is a owner of the barter
        if request.user != barter.owner:
            return redirect('generics:forbidden')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
