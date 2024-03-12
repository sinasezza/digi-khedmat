from django import forms
from django.contrib.auth.hashers import make_password
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import CaptchaField
from . import models


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        model = models.Account
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password')
        
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره تلفن',
            'email': 'ایمیل',
            'password': 'رمز عبور',
            'confirm_password': 'تایید رمز عبور', 
        }
        
        help_texts = {
            'username': 'حداکثر 25 کاراکتر وارد کنید.',
            'first_name': 'حداکثر 20 کاراکتر وارد کنید.',
            'last_name': 'حداکثر 20 کاراکتر وارد کنید.',
            'phone_number': 'یک شماره تلفن معتبر مانند 09909900000 کنید. حداکثر 20 کاراکتر.',
            'email': 'لطفا یک ایمیل معتبر مانند something@company.com حداکثر 60 کاراکتر وارد کنید.',
            'password': 'رمز عبور حداقل 8 حرف و حداکثر 30 حرف باشد',
            'confirm_password': 'تایید رمز عبور', 
        }
    
    # ---------------------------------------------------
    
    def clean_username(self):
        username = self.cleaned_data['username']
        matching_usernames = models.Account.objects.filter(username=username)
        if not username or username == "":
            raise forms.ValidationError('لطفا نام کاربری خود را به درستی وارد کنید.')
        if len(username) > 25:
            raise forms.ValidationError('نام کاربری حداکثر میتواند 25 حرف داشته باشد.')
        if matching_usernames.exists():
            raise forms.ValidationError('این نام کاربری در سیستم وجود دارد.')
        
        return username
    
    # ---------------------------------------------------
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if len(first_name) > 20:
            raise forms.ValidationError('نام حداکثر 20 حرف میتواند داشته  باشد.')
    
    # ---------------------------------------------------
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if len(last_name) > 20:
            raise forms.ValidationError('نام خانوادگی 20 حرف میتواند داشته  باشد.')
    
    # ---------------------------------------------------
    
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        
        if len(password1) > 30:
            raise forms.ValidationError('طول رمز حداکثر 30 حرف است.')
        if not password1 == password2 :
            raise forms.ValidationError('رمز عبور و تاییدیه رمز هماهنگ نیستند')

        return password1, password2
    
    # ---------------------------------------------------
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        matching_phone_numbers = models.Account.objects.filter(phone_number=phone_number)

        if len(phone_number) > 20:
            raise forms.ValidationError('حداکثر طول شماره تلفن 20 شماره است.')
        if matching_phone_numbers.exists():
            raise forms.ValidationError('این شماره تلفن در سامانه وجود دارد.')
        
        return phone_number

    # ---------------------------------------------------
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        matching_emails = models.Account.objects.filter(email=email)

        if len(email) > 60:
            raise forms.ValidationError('حداکثر طول ایمیل 60 حرف است.')
        if matching_emails.exists():
            raise forms.ValidationError('این ایمیل در سامانه وجود دارد.')
        
        return email

    # ---------------------------------------------------

    def save(self, commit=True, *args, **kwargs):
        new_account = super().save(commit=False, *args, **kwargs)
        new_account.set_password(self.cleaned_data.get('password'))
        new_account.is_active = False  # Set is_active to False for new users
        
        if commit:
            new_account.save()
        return new_account

# ======================================================

class UserRegisterInfoForm(forms.ModelForm):    
    
    class Meta:
        model = models.Account
        fields = ('age', 'gender', 'national_code', 'bio', 'education', 'occupation', 'company_name', 'address')
        
        labels = {
            'age': 'سن',
            'gender': 'جنسیت',
            'national_code': 'کد ملی',
            'bio': 'درباره شما',
            'education': 'تحصیلات', 
            'occupation': 'شغل', 
            'company_name': 'نام شرکت', 
            'address': 'آدرس', 
        }
        
        help_texts = {
            'age': 'حداکثر 100',
            'gender': 'جنسیت',
            'national_code': '10 کاراکتر و عددی',
            'bio': 'حداکثر 250 کاراکتر',
            'education': 'حداکثر 50 کاراکتر', 
            'occupation': 'حداکثر 40 کاراکتر', 
            'company_name': 'حداکثر 50 کاراکتر', 
            'address': 'حداکثر 90 کاراکتر', 
        }
        
    def clean_age(self):
        age = int(self.cleaned_data.get('age'))
        if not 0 < age <= 100:
            raise forms.ValidationError('سن باید عددی بین 1 و 100 باشد.')
        return age
    
    def save(self, commit=True, *args, **kwargs) -> models.Account:
        info_complete = kwargs.pop('info_complete', None)
        user = super().save(commit=False, *args, **kwargs)
        
        if info_complete:
            user.info_complete = True
        
        user.save()
        
        return user


# ======================================================

class UserLoginForm(forms.Form):
    identifier = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()
    
    
# ======================================================

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = models.Account
        fields = ('username', 'profile_photo', 'first_name', 'last_name', 'phone_number', 'email')
        
        help_texts = {
            'username': 'حداکثر 25 کاراکتر وارد کنید.',
            'first_name': 'حداکثر 20 کاراکتر وارد کنید.',
            'last_name': 'حداکثر 20 کاراکتر وارد کنید.',
            'phone_number': 'یک شماره تلفن معتبر مانند 09909900000 کنید. حداکثر 20 کاراکتر.',
            'email': 'لطفا یک ایمیل معتبر مانند something@company.com حداکثر 60 کاراکتر وارد کنید.',
        }

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
