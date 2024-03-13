from typing import Any
from django import forms
from ckeditor.widgets import CKEditorWidget
from . import models


class JobAdvertisingForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = models.JobAdvertising
        fields = (
            'title',
            'summary',
            'description',
            'status',
            'gender',
            'age_range',
            'skills',
            'study_grade',
            'benefits',
            'work_time',
            'military_service',
            'region',
            'address',
        )
        
        labels = {
            'title': 'عنوان آگهی',
            'summary': 'خلاصه آگهی',
            'description': 'توضیحات',
            'status': 'وضعیت آگهی',
            'gender': 'جنسیت',
            'age_range': 'بازه سنی',
            'skills': 'الزامات/مهارت ها',
            'study_grade': 'حداقل مدرک تحصیلی',
            'benefits': 'مزایا',
            'work_time': 'ساعت کاری',
            'military_service': 'وضعیت سربازی',
            'region': 'منطقه',
            'address': 'آدرس',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 20:
            raise forms.ValidationError('عنوان آگهی باید حداکثر 20 حرف باشد.')
        return title
    
    # --------------------------------------------------------
    
    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if summary and len(summary) > 25:
            raise forms.ValidationError('خلاصه آگهی باید حداکثر 25 حرف باشد.')
        return summary
    
    # --------------------------------------------------------
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 2000:
            raise forms.ValidationError('توضیحات باید حداکثر 2000 حرف باشد.')
        return description
    
    # --------------------------------------------------------
    
    def clean_age_range(self):
        age_range = self.cleaned_data.get('age_range')
        if age_range and len(age_range) > 30:
            raise forms.ValidationError('بازه سنی باید حداکثر 30 حرف باشد.')
        return age_range
    
    # --------------------------------------------------------
    
    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if skills and len(skills) > 200:
            raise forms.ValidationError('مهارت ها باید حداکثر 200 حرف باشد.')
        return skills
    
    # --------------------------------------------------------
    
    def clean_benefits(self):
        benefits = self.cleaned_data.get('benefits')
        if benefits and len(benefits) > 200:
            raise forms.ValidationError('مزایا باید حداکثر 200 حرف باشد.')
        return benefits
    
    # --------------------------------------------------------
    
    def clean_work_time(self):
        work_time = self.cleaned_data.get('work_time')
        if work_time and len(work_time) > 50:
            raise forms.ValidationError('ساعت کاری باید حداکثر 50 حرف باشد.')
        return work_time
    
    # --------------------------------------------------------
    
    def clean_military_service(self):
        military_service = self.cleaned_data.get('military_service')
        if military_service and len(military_service) > 50:
            raise forms.ValidationError('وضعیت سربازی باید حداکثر 20 حرف باشد.')
        return military_service
    
    # --------------------------------------------------------
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) > 55:
            raise forms.ValidationError("حداکثر طول آدرس باید 55 حرف باشد.")
        return address

# ================================================================

class ResumeFileForm(forms.ModelForm):
    
    class Meta:
        model = models.ResumeFile
        fields = (
            'fname',
            'lname',
            'title',
            'description',
            'pdf_file',
        )
    
    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        if fname and len(fname) > 20:
            raise forms.ValidationError('طول نام نباید از 20 حرف بیشتر باشد.')
        return fname
    
    # -------------------------------------------------------------
    
    def clean_lname(self):
        lname = self.cleaned_data.get('lname')
        if lname and len(lname) > 20:
            raise forms.ValidationError('طول نام خانوادگی نباید بیش از 20 حرف باشد.')
        return lname
    
    # -------------------------------------------------------------
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 20:
            raise forms.ValidationError('طول عنوان نباید بیش از 20 حرف باشد.')
        return title
    
    # -------------------------------------------------------------
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 250:
            raise forms.ValidationError('طول توضیحات نباید بیش از 250 حرف باشد.')
        return description




# ================================================================

class ResumeForm(forms.ModelForm):
    
    fname = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True, 'disabled': True,}), label='نام')
    lname = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True, 'disabled': True,}), label='نام خانوادگی')
    title = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True, 'disabled': True,}), label='عنوان')
    description = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 250, 'required': True, 'disabled': True,}), label='توضیحات')
    gender = forms.ChoiceField(widget=forms.Select(attrs={'disabled': True}), choices=models.JobAdvertising.GENDERS)
    military_service = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 25, 'required': True, 'disabled': True,}), label='وضعیت سربازی')
    telephone = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True, 'disabled': True,}), label='شماره تلفن')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'maxlength': 50, 'required': True, 'disabled': True,}), label='ایمیل')
    linkedin = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 255, 'disabled': True,}), label='لینکدین')
    github = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 255, 'disabled': True,}), label='گیت‌هاب')
    website = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 150, 'disabled': True,}), label='وب‌سایت')
    
    class Meta:
        model = models.Resume
        fields = (
            'fname',
            'lname',
            'title',
            'description',
            'gender',
            'military_service',
            'image',
            'telephone',
            'email',
            'linkedin',
            'github',
            'website',
        )

    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        if fname and len(fname) > 20:
            raise forms.ValidationError('طول نام نباید از 20 حرف بیشتر باشد.')
        return fname
    
    # ------------------------------------------------------------------

    def clean_lname(self):
        lname = self.cleaned_data.get('lname')
        if lname and len(lname) > 20:
            raise forms.ValidationError('طول نام خانوادگی نباید بیش از 20 حرف باشد.')
        return lname
    
    # ------------------------------------------------------------------

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 20:
            raise forms.ValidationError('طول عنوان نباید بیش از 20 حرف باشد.')
        return title
    
    # ------------------------------------------------------------------

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 250:
            raise forms.ValidationError('طول توضیحات نباید بیش از 250 حرف باشد.')
        return description

    # ------------------------------------------------------------------

    def clean_military_service(self):
        military_service = self.cleaned_data.get('military_service')
        if military_service and len(military_service) > 25:
            raise forms.ValidationError('وضعیت سربازی نباید بیش از 25 حرف باشد.')
        return military_service
    
    # ------------------------------------------------------------------

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone and len(telephone) > 20:
            raise forms.ValidationError('شماره تلفن نباید بیش از 20 حرف باشد.')
        return telephone

    # ------------------------------------------------------------------

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and len(email) > 50:
            raise forms.ValidationError('طول توضیحات نباید بیش از 50 حرف باشد.')
        return email

    # ------------------------------------------------------------------

    def clean_linkedin(self):
        linkedin = self.cleaned_data.get('linkedin')
        if linkedin and len(linkedin) > 255:
            raise forms.ValidationError('آدرس لیندکدین نباید بیش از 255 حرف باشد.')
        return linkedin

    # ------------------------------------------------------------------

    def clean_github(self):
        github = self.cleaned_data.get('github')
        if github and len(github) > 255:
            raise forms.ValidationError('آدرس گیتهاب نباید بیش از 255 حرف باشد.')
        return github

    # ------------------------------------------------------------------

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and len(website) > 150:
            raise forms.ValidationError('آدرس وبسایت نباید بیش از 150 حرف باشد.')
        return website

        
# ================================================================

class ExperienceForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True}), label='عنوان')
    company = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 35, 'required': True}), label='شرکت/مجموعه')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'required': True}), label='تاریخ شروع')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='تاریخ پایان')
    description = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 100, 'required': True}), label='توضیحات')
    
    class Meta:
        model = models.Experience
        fields = (
            'title',
            'company',
            'start_date',
            'end_date',
            'description',
        )

    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date > end_date :
            raise forms.ValidationError('تاریخ شروع از تاریخ پایان بیشتر است.')

        return  cleaned_data

    # ------------------------------------------------------------------
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 20:
            raise forms.ValidationError("حداکثر طول عنوان باید 20 حرف باشد.")
        return title
    
    # ------------------------------------------------------------------
    
    def clean_company(self):
        company = self.cleaned_data.get('company')
        if len(company) > 35:
            raise forms.ValidationError("حداکثر طول شرکت/مجموعه باید 35 حرف باشد.")
        return company

    # ------------------------------------------------------------------

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 100:
            raise forms.ValidationError("حداکثر طول توضیحات باید 100 حرف باشد.")
        return description

# ================================================================

class SkillForm(forms.ModelForm):
    
    title = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True}), label='عنوان')
    
    class Meta:
        model = models.Skill
        fields = (
            'title',
        )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 20:
            raise forms.ValidationError("حداکثر طول عنوان باید 20 حرف باشد.")
        return title

# ================================================================

class EducationForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True}), label='عنوان')
    description = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 100, 'required': True}), label='توضیحات')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'required': True}), label='تاریخ شروع')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='تاریخ پایان')
    
    class Meta:
        model = models.Education
        fields = (
            'title',
            'description',
            'start_date',
            'end_date',
        )

    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date > end_date :
            raise forms.ValidationError('تاریخ شروع از تاریخ پایان بیشتر است.')

        return  cleaned_data

    # ------------------------------------------------------------------
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 20:
            raise forms.ValidationError("حداکثر طول عنوان باید 20 حرف باشد.")
        return title

    # ------------------------------------------------------------------

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 100 :
            raise forms.ValidationError("حداکثر طول توضیحات باید 100 حرف باشد.")
        return description

# ================================================================

class AchievementForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True}), label='عنوان')
    description = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 100, 'required': True}), label='توضیحات')

    class Meta:
        model = models.Achievement
        fields = (
            'title',
            'description',
        )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 20 :
            raise forms.ValidationError("حداکثر طول عنوان باید 20 حرف باشد.")
        return title

    # ------------------------------------------------------------------

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 100 :
            raise forms.ValidationError("حداکثر طول توضیحات باید 100 حرف باشد.")
        return description

# ================================================================

class LanguageForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 20, 'required': True}), label='نام')
    level = forms.ChoiceField(widget=forms.Select(attrs={'required': True}), choices=models.Language.LEVELS, label='سطح')

    class Meta:
        model = models.Language
        fields = (
            'name',
            'level',
        )
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 20 :
            raise forms.ValidationError("حداکثر طول نام باید 20 حرف باشد.")
        return name