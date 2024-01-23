from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from . import models, forms


def stuff_list_view(request):
    stuffs = models.Stuff.objects.filter(status='published')
    
    context = {
        'stuffs': stuffs,
    }
    return render(request, 'barter/stuff-list.html', context)

# ---------------------------------------------------------

def stuff_detail_view(request: HttpRequest, stuff_id: str, stuff_slug: str):
    try:
        stuff = models.Stuff.objects.get(id=stuff_id)
    except:
        return render(request, 'common/404.html')
    
    if stuff.status == 'draft':
        return HttpResponse("این آگهی پیدا نشده یا در دست ساخت است.")
    
    context = {
        'stuff': stuff,
    }
    return render (request, 'barter/stuff-detail.html', context)

# ---------------------------------------------------------

def stuff_update_view(request: HttpRequest, stuff_id: str, stuff_slug: str):
    try:
        stuff = models.Stuff.objects.get(id=stuff_id)
    except:
        return render(request, 'common/404.html')
    
    if not stuff.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    context = {
        
    }
    
    return render(request, 'barter/stuff-update.html', context)
# ---------------------------------------------------------

def stuff_delete_view(request: HttpRequest, stuff_id: str, stuff_slug: str):
    stuff = models.Stuff.objects.get(id=stuff_id)
    
    if not stuff.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    stuff.delete()
    
    return reverse_lazy("barter:stuff-list")
    
# ---------------------------------------------------------