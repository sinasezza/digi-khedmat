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
            
            # "categories",
            # "tags",
            # "locations",
        )

# =====================================================
