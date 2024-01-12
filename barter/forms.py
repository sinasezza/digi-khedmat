from django import forms
from . import models


class StuffCreationForm(forms.ModelForm):
    
    class Meta:
        model = models.Stuff
        fields = (
            "title",
            "summary",
            "description",
            "category",
            "tags",
            "location",
        )