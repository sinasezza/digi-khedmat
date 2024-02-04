from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def handler404(request, *args, **argv):
    return render(request, 'common/404.html', status=404)

# ---------------------------------------------------------


def handler500(request, *args, **argv):
    return render(request, 'common/500.html', status=500)

# ---------------------------------------------------------

def main_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'generics/home-page.html')