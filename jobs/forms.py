from django import forms
from . import models


class JobAdvertisingForm(forms.ModelForm):
    
    class Meta:
        model = models.JobAdvertising
        fields = (
            "title",
        )