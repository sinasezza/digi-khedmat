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
        
        error_messages = {
            'title': {
                'max_length': "حداکثر طول عنوان باید 20 حرف باشد.",
            },
            'summary': {
                'max_length': "حداکثر طول معاوضه باید 25 حرف باشد.",
            },
            'address': {
                'max_length': "حداکثر طول آدرس باید 55 حرف باشد.",
            },
        }
    
    # ----------------------------------------------
    
    def clean_title(self):
        title: str = self.cleaned_data.get('title')
        if len(title) > 20:
            raise forms.ValidationError("حداکثر طول عنوان باید 20 حرف باشد.")
        return title
    
    # ----------------------------------------------
    
    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if summary and len(summary) > 25:
            raise forms.ValidationError("حداکثر طول معاوضه باید 25 حرف باشد.")
        return summary
    
    # ----------------------------------------------
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 2000:
            raise forms.ValidationError('توضیحات باید حداکثر 2000 حرف باشد.')
        return description
    
    # --------------------------------------------------------
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) > 55:
            raise forms.ValidationError("حداکثر طول آدرس باید 55 حرف باشد.")
        return address

# =====================================================

class BarterImageForm(forms.ModelForm):
    
    class Meta:
        model = models.BarterImage 
        fields = ('image' ,)
