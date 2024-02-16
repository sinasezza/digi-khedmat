from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
# from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from django.views.generic.edit import CreateView
# from django.contrib.auth.views import LoginView
from django.utils import timezone
from . import models, forms, utils


def register_view(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"حساب کاربری با موفقیت ایجاد شد.")
            return redirect('accounts:login')
        else:
            print(f"error {form.errors.as_data}")
            messages.warning(request, 'لطفا فرم را صحیح تر پر کنید.')
            form = forms.UserRegisterForm(request.POST)
    else:
        form = forms.UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html',context)
            


# ---------------------------------------------------
 
def login_view(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('generics:main-page')
        else:
            print(f"error : {form.errors.as_data()}")
    else:
        form = forms.UserLoginForm()
    context = {'form': form,}
    return render(request, 'accounts/login.html', context)

# ---------------------------------------------------

def login_otp_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')
                
        user = utils.find_phone_number_owner(phone_number)
        
        if user is not None:
            otp_obj = models.OneTimePassword.objects.filter(user=user, code=otp, created_at__gt=timezone.now() - timezone.timedelta(minutes=2)).last()            
            if otp_obj and otp_obj.code == otp:
                login(request, otp_obj.user)
                otp_obj.delete()
                return redirect('generics:main-page')
            else:
                messages.error(request, 'کد نادرست است و یا منقضی شده است.')             
        else:
            messages.error(request, 'کد نادرست است و یا منقضی شده است.')             
            
    
    return render(request, 'accounts/login-otp.html')

# ---------------------------------------------------

@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# ---------------------------------------------------


@login_required(login_url='accounts:login')
def user_panel_view(request):
    """View for the user panel page."""
    barters = request.user.barters.filter(status='published').order_by('-date_created')
    jobs = request.user.jobs.all().order_by('-date_created')
    # ads = request.user.ads.all().order_by('-date_created')
    
    context = {
        'barters': barters,
        'jobs': jobs,
        # 'ads': ads,
    }
    return render(request, 'accounts/user-panel.html', context)


# ---------------------------------------------------

@login_required(login_url='accounts:login')
def my_profile_view(request: HttpRequest) -> HttpResponse:
    """View for the user profile page."""
    
    context = {}
    return render(request, 'accounts/my-profile.html', context)

# ---------------------------------------------------

def user_profile_view(request: HttpRequest, id: str) -> HttpResponse:
    user = get_object_or_404(models.Account, id=id)
    
    context = {
        'user': user,
    }
    return render(request, 'accounts/user-profile.html', context)

# ---------------------------------------------------

@login_required(login_url='accounts:login')
def notifications_view(request: HttpRequest) -> HttpResponse:
    notifications = models.Notification.objects.filter(recipient=request.user)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'accounts/notifications.html', context)

# ---------------------------------------------------

@login_required(login_url='accounts:login')
def favorites_view(request: HttpRequest) -> HttpResponse:
    
    favorites = request.user.favorites.order_by('-date_created')
    context = {
        'favorites': favorites
    }
    return render(request, 'accounts/favorites.html', context)