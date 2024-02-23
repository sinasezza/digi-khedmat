from django.contrib import admin
from django.utils.html import mark_safe
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from . import models


class StuffImageInline(admin.StackedInline):
    model = models.StuffImage
    extra = 1
    ordering = ('-id',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{0}" style="max-width:200px;max-height:200px" />'.format(obj.image.url))
        else:
            return '-'

    image_tag.short_description = 'Image Preview'

class StuffAdvertisingResource(resources.ModelResource):
    class Meta:
        model = models.StuffAdvertising
        
@admin.register(models.StuffAdvertising)
class StuffAdvertisingAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title')
    
    inlines = [StuffImageInline,]
    resource_classes = [StuffAdvertisingResource,]
    
# ==================================================================

@admin.register(models.StuffImage)
class StuffImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'stuff_advertising','image')

# ==================================================================

@admin.register(models.BusinessAdvertising)
class BusinessAdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business_type')

# ==================================================================

@admin.register(models.BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'business_advertising')