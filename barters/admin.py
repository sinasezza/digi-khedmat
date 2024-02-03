from django.contrib import admin
from . import models


@admin.register(models.BarterAdvertising)
class BarterAdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'date_created', 'status',)
    ordering = ['-date_created',]

# ================================================
    
@admin.register(models.BarterImage)
class BarterImageAdmin(admin.ModelAdmin):
    list_display = ('title','image')

# ================================================
