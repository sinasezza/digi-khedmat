from django import forms
from . import models


class JobAdvertisingForm(forms.ModelForm):
    
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