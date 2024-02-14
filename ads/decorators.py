from django.shortcuts import render, redirect, get_object_or_404
from . import models

def owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        adv_slug = kwargs.get('adv_slug')
        barter = get_object_or_404(models.StuffAdvertising, slug=adv_slug)
                
        # Check if the user is a owner of the advertisement
        if request.user != barter.owner:
            return redirect('generics:forbidden')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
