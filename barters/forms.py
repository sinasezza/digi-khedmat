from django import forms
from . import models


class BarterForm(forms.ModelForm):
    # images = ???
    
    class Meta:
        model = models.BarterAdvertising
        fields = (
            "title",
            "summary",
            "description",
            "categories",
            "tags",
            "locations",
        )