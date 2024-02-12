from django.shortcuts import render, redirect, get_object_or_404
from . import models

def owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        barter_slug = kwargs.get('barter_slug')
        barter = get_object_or_404(models.BarterAdvertising, slug=barter_slug)
                
        # Check if the user is a owner of the barter
        if request.user != barter.owner:
            return redirect('generics:not-found')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
