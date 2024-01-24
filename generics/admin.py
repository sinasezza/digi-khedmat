from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_type')

# ================================================

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ================================================

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('province', 'city', 'address',)

# ================================================