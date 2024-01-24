from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views import generic
from . import models, forms


# def barter_list_view(request):
#     barters = models.BarterAdvertising.objects.filter(status='published')
    
#     context = {
#         'barters': barters,
#     }
#     return render(request, 'barters/barter-list.html', context)

# ---------------------------------------------------------

class BarterListView(generic.ListView):
    model = models.BarterAdvertising
    queryset = models.BarterAdvertising.objects.filter(status='published')
    template_name = "barters/barter-list.html"
    context_object_name = 'barters'

# ---------------------------------------------------------


# def barter_detail_view(request: HttpRequest, barter_id: str, barter_slug: str):
#     try:
#         barter = models.BarterAdvertising.objects.get(id=barter_id)
#     except:
#         return render(request, 'common/404.html')
    
#     if barter.status == 'draft':
#         return HttpResponse("این آگهی پیدا نشده یا در دست ساخت است.")
    
#     context = {
#         'barter': barter,
#     }
#     return render (request, 'barters/barter-detail.html', context)

# ---------------------------------------------------------

class BarterDetailView(generic.DeleteView):
    model = models.BarterAdvertising
    queryset = models.BarterAdvertising.objects.filter(status='published')
    template_name = "barters/barter-list.html"
    pk_url_kwarg = 'barter_id'
    context_object_name = 'barter'
    
# ---------------------------------------------------------

def barter_update_view(request: HttpRequest, barter_id: str, barter_slug: str):
    try:
        barter = models.BarterAdvertising.objects.get(id=barter_id)
    except:
        return render(request, 'common/404.html')
    
    if not barter.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    context = {
        
    }
    
    return render(request, 'barters/barter-update.html', context)
# ---------------------------------------------------------

def barter_delete_view(request: HttpRequest, barter_id: str, barter_slug: str):
    barter = models.BarterAdvertising.objects.get(id=barter_id)
    
    if not barter.owner == request.user:
        return HttpResponse("شما دسترسی به این آگهی ندارید.")
    
    barter.delete()
    
    return reverse_lazy("barters:barter-list")
    
# ---------------------------------------------------------