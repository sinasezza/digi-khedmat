from django import forms
from django.forms.models import inlineformset_factory
from ckeditor.widgets import CKEditorWidget
from . import models



class BarterForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = models.BarterAdvertising
        fields = (
            "title",
            "summary",
            "description",
            "status",
            "region",
            "address",
            "categories",
            "tags",
        )

# =====================================================

BarterImagesFormSet = inlineformset_factory(
    models.BarterAdvertising,
    models.BarterImage,
    fields=('image',),  # Adjust fields as needed
    extra=4,  # No additional empty forms
    can_delete=False,  # Allow deletion of existing forms
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    }
)

