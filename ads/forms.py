from django import forms
from . import models
from django.forms.models import inlineformset_factory


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
        )

StuffImagesFormSet = inlineformset_factory(
    models.StuffAdvertising,
    models.StuffImage,
    fields=('image',),  # Adjust fields as needed
    extra=4,  # No additional empty forms
    can_delete=False,  # Allow deletion of existing forms
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    }
)

