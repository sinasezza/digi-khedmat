from django.shortcuts import render, redirect, get_object_or_404
from . import models

def member_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        room_name = kwargs.get('room_name')
        thread = get_object_or_404(models.Thread, name=room_name)
                
        # Check if the sender is a member of the thread
        if request.user not in (thread.user1, thread.user2):
            return redirect('generics:not-found')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
