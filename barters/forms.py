from django import forms
from django.forms.models import inlineformset_factory
from . import models



class BarterForm(forms.ModelForm):
    # images = ???
    
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
