from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_page


@cache_page(60 * 1440)  # 1 day
def handler404(request, *args, **argv):
    return render(request, 'common/404.html', status=404)

# ---------------------------------------------------------

@cache_page(60 * 1440)  # 1 day
def handler500(request, *args, **argv):
    return render(request, 'common/500.html', status=500)

# ---------------------------------------------------------

def main_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'generics/home-page.html')

# ---------------------------------------------------------

@cache_page(60 * 1440)  # 1 day
def about_us_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'generics/about-us.html', context)

# ---------------------------------------------------------

@cache_page(60 * 1440)  # 1 day
def privacy_policy_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'generics/privacy-policy.html', context)

# ---------------------------------------------------------

@cache_page(60 * 1440)  # 1 day
def certificates_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'generics/certificates.html', context)

# ---------------------------------------------------------

@cache_page(60 * 1440)  # 1 day
def contact_us_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'generics/contact-us.html', context)

# ---------------------------------------------------------
