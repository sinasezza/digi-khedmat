from django.shortcuts import render


def handler404(request, *args, **argv):
    return render(request, 'common/404.html', status=404)


def handler500(request, *args, **argv):
    return render(request, 'common/500.html', status=500)