from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from . import models


@admin.register(models.JobCategory)
class JobCategoryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title',)

# ================================================

@admin.register(models.StuffCategory)
class StuffCategoryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title',)

# ================================================

@admin.register(models.Tag)
class TagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name',)

# ================================================

class RegionResource(resources.ModelResource):
    class Meta:
        model = models.Region

# ================================================

@admin.register(models.Region)
class RegionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('state', 'city',)
    
    resource_classes = [RegionResource,]

# ================================================

class ContactResource(resources.ModelResource):
    class Meta:
        model = models.Contact

# ================================================

@admin.register(models.Contact)
class ContactAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user', 'fname', 'lname', 'company_name', 'phone_number', 'email',)
    
    resource_classes = [ContactResource,]

# ================================================

@admin.register(models.SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'media_type', 'link')