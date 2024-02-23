from django.contrib import admin
from django.utils.html import mark_safe
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from . import models


class BarterImageInline(admin.StackedInline):
    model = models.BarterImage
    extra = 1
    ordering = ('-id',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{0}" style="max-width:200px;max-height:200px" />'.format(obj.image.url))
        else:
            return '-'

    image_tag.short_description = 'Image Preview'

class BarterResource(resources.ModelResource):
    class Meta:
        model = models.BarterAdvertising
        
@admin.register(models.BarterAdvertising)
class BarterAdvertisingAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id','title', 'date_created', 'status',)
    search_fields = ('id', 'title',)
    list_filter = ('owner', 'status', 'tags', 'categories', 'region')
    ordering = ('-date_created',)
    
    inlines = [BarterImageInline,]
    resource_classes = [BarterResource,]

# ================================================
    
@admin.register(models.BarterImage)
class BarterImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'barter_advertising')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{0}" style="max-width:200px;max-height:200px" />'.format(obj.image.url))
        else:
            return '-'

    image_tag.short_description = 'Image Preview'

# ================================================
