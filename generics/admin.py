from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_type')

# ================================================

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

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

@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('region', 'address',)

# ================================================

class ContactResource(resources.ModelResource):
    class Meta:
        model = models.Contact

# ================================================

@admin.register(models.Contact)
class ContactAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user', 'fname', 'lname', 'company_name', 'phone_number', 'email',)
    
    resource_classes = [ContactResource,]