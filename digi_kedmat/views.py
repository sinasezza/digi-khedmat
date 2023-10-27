from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def main_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/home_page.html')