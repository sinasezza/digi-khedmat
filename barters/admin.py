from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from . import models



class BarterResource(resources.ModelResource):
    class Meta:
        model = models.BarterAdvertising
        
@admin.register(models.BarterAdvertising)
class BarterAdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'date_created', 'status',)
    ordering = ['-date_created',]
    
    resource_classes = [BarterResource,]

# ================================================
    
@admin.register(models.BarterImage)
class BarterImageAdmin(admin.ModelAdmin):
    list_display = ('title','image', 'barter_advertising')

# ================================================
