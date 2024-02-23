from django import forms
from django.forms.models import inlineformset_factory
from . import models


class StuffAdvertisingForm(forms.ModelForm):
    
    class Meta:
        model = models.StuffAdvertising
        fields = (
            'title',
            'summary',
            'description',
            'status',
            'price',
            'stuff_status',
            'region',
            'address',
        )



