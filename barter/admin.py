from django.contrib import admin
from . import models


@admin.register(models.Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ('id','title')

# ================================================

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_type')

# ================================================

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ================================================
    
@admin.register(models.StuffImage)
class StuffImageAdmin(admin.ModelAdmin):
    list_display = ('title','image')

# ================================================
