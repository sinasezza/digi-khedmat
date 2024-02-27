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
            'image',
            'telephone',
            'email',
            'linkedin',
            'github',
            'website',
        )