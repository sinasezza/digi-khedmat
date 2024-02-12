from django import forms
from . import models


class StuffAdvertisingForm(forms.ModelForm):
    
    class Meta:
        model = models.StuffAdvertising
        fields = (
            'price',
        )