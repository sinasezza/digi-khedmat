from django import forms
from . import models


class StuffForm(forms.ModelForm):
    # images = ???
    
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