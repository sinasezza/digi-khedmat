from django import forms
from . import models


class ContactForm(forms.ModelForm):
    
    class Meta:
        model = models.Contact
        fields = '__all__'
        exclude = ('user',)
        
    def clean_message(self):
        message = self.cleaned_data.get('message')

        if message and len(message) > 450:
            raise forms.ValidationError("طول پیام باید حداکثر 450 حرف باشد.")