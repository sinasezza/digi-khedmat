from django import forms
from django.contrib.auth.hashers import make_password
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import CaptchaField
from . import models


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        model = models.Account
        fields = ('username', 'first_name', 'last_name', 'phone_number','password', 'confirm_password')
        
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره تلفن',
            'password': 'رمز عبور',
            'confirm_password': 'تایید رمز عبور', 
        }
    
    # ---------------------------------------------------
    
    def clean_username(self):
        username = self.cleaned_data['username']
        matching_usernames = models.Account.objects.filter(username=username)
        if not username or username == "":
            raise forms.ValidationError('لطفا نام کاربری خود را به درستی وارد کنید.')
        if len(username) > 150:
            raise forms.ValidationError('نام کاربری حداکثر میتواند ۱۵۰ کاراکتر داشته باشد.')
        if matching_usernames.exists():
            raise forms.ValidationError('این نام کاربری در سیستم وجود دارد.')
        
        return username
    
    # ---------------------------------------------------
    
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
                
        if not password1 == password2 :
            raise forms.ValidationError('رمز عبور و تاییدیه رمز هماهنگ نیستند')
        
        return password1, password2
    
    # ---------------------------------------------------
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        matching_phone_numbers = models.Account.objects.filter(phone_number=phone_number)

        if matching_phone_numbers.exists():
            raise forms.ValidationError('این شماره تلفن وجود دارد.')
        
        return phone_number

    # ---------------------------------------------------

    def save(self, commit=True, *args, **kwargs):
        new_account = super().save(commit=False, *args, **kwargs)
        new_account.set_password(self.cleaned_data.get('password'))
        
        if commit:
            new_account.save()
        return new_account

# ======================================================

class UserRegisterInfoForm(forms.ModelForm):    
    
    class Meta:
        model = models.Account
        fields = ('profile_photo', 'age', 'gender', 'national_code', 'bio', 'education', 'occupation', 'company_name', 'address')
        
        labels = {
            'profile_photo': 'عکس پروفایل',
            'age': 'سن',
            'gender': 'جنسیت',
            'national_code': 'کد ملی',
            'bio': 'درباره شما',
            'education': 'تحصیلات', 
            'occupation': 'شغل', 
            'company_name': 'نام شرکت', 
            'address': 'آدرس', 
        }
    
    def save(self, commit=True, *args, **kwargs) -> models.Account:
        info_complete = kwargs.pop('info_complete', None)
        user = super().save(commit=False, *args, **kwargs)
        
        if info_complete:
            user.info_complete = True
        
        user.save()
        
        return user


# ======================================================

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()
    

# ======================================================

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = models.Account
        fields = ('username', 'profile_photo', 'first_name', 'last_name', 'phone_number', 'email')

# ======================================================

class ChangePasswordForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        self.user : models.Account = user
        super().__init__(*args, **kwargs)

    old_pass =  forms.CharField(label="گذرواژه قبل", widget=forms.PasswordInput())
    new_pass1 = forms.CharField(label="گذرواژه جدید", widget=forms.PasswordInput())
    new_pass2 = forms.CharField(label="تکرار گذرواژه جدید", widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super().clean()
        old_pass = cleaned_data.get('old_pass')
        new_pass1 = cleaned_data.get("new_pass1")
        new_pass2 = cleaned_data.get("new_pass2")
        
        print(f"old pass is {old_pass}")
        if not self.user.check_password(old_pass):
            raise forms.ValidationError("گذرواژه قبل  اشتباه است.")
        
        if new_pass1 and new_pass2:
            if new_pass1 != new_pass2:
                raise forms.ValidationError("گذرواژه جدید و تکرار آن مطابقت ندارن.")
                
        return cleaned_data 
