from django.contrib import admin
from . import models


@admin.register(models.StuffAdvertising)
class StuffAdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    
# ==================================================================

@admin.register(models.BusinessAdvertising)
class BusinessAdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business_type')

# ==================================================================

@admin.register(models.BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image',)