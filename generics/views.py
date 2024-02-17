from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_page
from django.contrib import messages
from . import models, forms


@cache_page(60 * 900)  # 15 min
def handler404(request, *args, **argv):
    return render(request, 'generics/404.html', status=404)

# ---------------------------------------------------------

@cache_page(60 * 900)  # 15 min
def handler500(request, *args, **argv):
    return render(request, 'generics/500.html', status=500)

# ---------------------------------------------------------

@cache_page(60 * 900)  # 15 min
def handler403(request, *args, **argv):
    return render(request, 'generics/403.html', status=403)

# ---------------------------------------------------------

@cache_page(60 * 900)  # 15 min
def main_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'generics/home-page.html')

# ---------------------------------------------------------

@cache_page(60 * 900)  # 15 min
def about_us_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'generics/about-us.html', context)

# ---------------------------------------------------------

@cache_page(60 * 900)  # 15 min
def privacy_policy_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'generics/privacy-policy.html', context)

# ---------------------------------------------------------

@cache_page(60 * 900)  # 15 min
def certificates_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'generics/certificates.html', context)

# ---------------------------------------------------------

@cache_page(60 * 900)  # 15 min
def contact_us_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            new_message = form.save()
            if request.user.is_authenticated:
                new_message.user = request.user
                new_message.save()
            messages.success(request, 'پیام شما توسط ما دریافت شد. به زودی با شما تماس میگیریم.')
            return redirect('generics:contact-us')
        else:
            messages.error(request, 'مشکلی پیش آمده. دوباره تلاش کنید.')
            form = forms.ContactForm(request.POST)
    else:
        form = forms.ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'generics/contact-us.html', context)

# ---------------------------------------------------------
