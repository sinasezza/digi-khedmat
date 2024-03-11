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

# ================================================================

class ResumeForm(forms.ModelForm):
    
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
        
# ================================================================

class ExperienceForm(forms.ModelForm):
    
    class Meta:
        model = models.Experience
        fields = (
            'title',
            'company',
            'start_date',
            'end_date',
            'description',
        )

# ================================================================

class SkillForm(forms.ModelForm):
    
    class Meta:
        model = models.Skill
        fields = (
            'title',
        )

# ================================================================

class EducationForm(forms.ModelForm):
    
    class Meta:
        model = models.Education
        fields = (
            'title',
            'description',
            'start_date',
            'end_date',
        )

# ================================================================

class AchievementForm(forms.ModelForm):
    
    class Meta:
        model = models.Achievement
        fields = (
            'title',
            'description',
        )

# ================================================================

class LanguageForm(forms.ModelForm):
    
    class Meta:
        model = models.Language
        fields = (
            'name',
            'level',
        )