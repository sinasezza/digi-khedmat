from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
# from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
# from django.views.generic.edit import CreateView
# from django.contrib.auth.views import LoginView
from django.utils import timezone
from . import models, forms, utils, decorators


@decorators.logout_required
def register_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
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

@login_required(login_url='accounts:login')
def register_info_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == 'POST':
        form = forms.UserRegisterInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(info_complete=True)
            
            messages.info(request, f"اطلاعات شما ثبت شد.")
            return redirect('generics:main-page')
        else:
            print(f"error {form.errors.as_data}")
            messages.warning(request, 'لطفا فرم را صحیح تر پر کنید.')
            form = forms.UserRegisterInfoForm(request.POST, instance=request.user)
    else:
        form = forms.UserRegisterInfoForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/register-info.html',context) 

# ---------------------------------------------------

@decorators.logout_required
def login_view(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            
            user = utils.check_user(request, identifier)
            
            if user and user.check_password(password):
                if not user.is_active:
                    messages.warning(request, "حساب کاربری شما غیر فعال است. لطفا جهت فعال سازی اقدام کنید.")
                    return redirect('accounts:login')
                
                # Login the user in
                login(request, user)    
                messages.success(request, f"{user.first_name} عزیز خوش آمدی")

                return redirect('accounts:register-info') if not user.info_complete else redirect('generics:main-page')
            else:
                messages.error(request, 'نام کاربری یا رمز ورود نادرست است.')
        else:
            messages.error(request, 'لطفا کپچا را به درستی وارد کنید.')
            print(f"error : {form.errors.as_data()}")
    else:
        form = forms.UserLoginForm()
    context = {'form': form,}
    return render(request, 'accounts/login.html', context)

# ---------------------------------------------------

@decorators.logout_required
def activate_account_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')
                
        user = utils.find_phone_number_owner(phone_number)
        
        if user is not None:
            otp_obj = models.OneTimePassword.objects.filter(user=user, code=otp, created_at__gt=timezone.now() - timezone.timedelta(minutes=2)).last()            
            if otp_obj and otp_obj.code == otp:
                otp_obj.delete()
                
                # activate the user
                user.is_active = True
                user.save()
                
                messages.success(request, 'تبریک! شما حساب خود را در دیجی خدمت فعال کردید.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'کد نادرست است و یا منقضی شده است.')             
        else:
            messages.error(request, 'کد نادرست است و یا منقضی شده است.')             
            
    
    return render(request, 'accounts/activate-account.html')

# ---------------------------------------------------

@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# ---------------------------------------------------

@login_required(login_url='accounts:login')
def delete_account_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    user = request.user
    SENTENCE = f"اینجانب {user.username} حساب خود را حذف میکنم"
    
    if request.method == "POST":
        password = request.POST.get('password')
        sentence = request.POST.get('sentence')

        if user.check_password(password) and sentence == SENTENCE:
            user.delete()
            messages.info(request, f'حساب کاربری {user.username} حذف شد.')
            return redirect('generics:main-page')
        else:
            messages.warning(request, 'گذرواژه یا جمله وارد شده اشتباه است. لطفا دوباره تلاش کنید.')

    return render(request, 'accounts/delete-account.html')

# ---------------------------------------------------

@login_required(login_url='accounts:login')
def change_password_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_pass = form.cleaned_data.get('new_pass1')
            request.user.set_password(new_pass)
            request.user.save()
            # Update the user's session with the new password
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'رمز عبور شما تغییر کرد.')
            return redirect('accounts:my-profile')
        else:
            messages.warning(request, 'خطایی رخ داده')
    else:
        form = forms.ChangePasswordForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/change-password.html', context)

# ---------------------------------------------------

@login_required(login_url='accounts:login')
def user_panel_view(request):
    """View for the user panel page."""
    barters = request.user.barters.all().order_by('-date_created')
    jobs = request.user.jobs.all().order_by('-date_created')
    stuff_ads = request.user.stuff_ads.all().order_by('-date_created')
    
    context = {
        'barters': barters,
        'jobs': jobs,
        'stuff_ads': stuff_ads,
    }
    return render(request, 'accounts/user-panel.html', context)


# ---------------------------------------------------

@login_required(login_url='accounts:login')
def my_profile_view(request: HttpRequest) -> HttpResponse:
    """View for the user profile page."""
    if request.method == "POST":
        form = forms.UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.info(request, 'اطلاعات کاربری شما با موفقیت ذخیره سازی گردید')
            return redirect('accounts:my-profile')
        else:
            print(f"error : {form.errors.as_data()}")
            messages.error(request, 'خطایی رخ داد')
    else:
        form = forms.UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/my-profile.html', context)

# ---------------------------------------------------

def user_profile_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(models.Account, username=username)
    
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

# ---------------------------------------------------
