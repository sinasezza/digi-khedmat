from django import forms
from django.forms.models import inlineformset_factory
from ckeditor.widgets import CKEditorWidget
from . import models


class StuffAdvertisingForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), max_length=2000) 
    
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

    def clean_title(self):
            title = self.cleaned_data.get('title')
            if title and len(title) > 20:
                raise forms.ValidationError('عنوان آگهی باید حداکثر 20 حرف باشد.')
            return title
        
    # --------------------------------------------------------
    
    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if summary and len(summary) > 25:
            raise forms.ValidationError('خلاصه آگهی باید حداکثر 25 حرف باشد.')
        return summary
    
    # --------------------------------------------------------

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 2000:
            raise forms.ValidationError('توضیحات باید حداکثر 2000 حرف باشد.')
        return description
    
    # --------------------------------------------------------
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and len(price) > 15:
            raise forms.ValidationError('قیمت باید حداکثر 15 حرف باشد.')
        return price
    
    # --------------------------------------------------------

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and len(price) > 15:
            raise forms.ValidationError('قیمت باید حداکثر 15 حرف باشد.')
        return price
    
    # --------------------------------------------------------
    
    def clean_stuff_status(self):
        stuff_status = self.cleaned_data.get('stuff_status')
        if stuff_status and len(stuff_status) > 12:
            raise forms.ValidationError('وضعیت کالا باید حداکثر 12 حرف باشد.')
        return stuff_status
    
    # --------------------------------------------------------
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) > 55:
            raise forms.ValidationError("حداکثر طول آدرس باید 55 حرف باشد.")
        return address

    # --------------------------------------------------------
    