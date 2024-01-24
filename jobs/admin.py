from django.contrib import admin
from . import models


@admin.register(models.JobAdvertising)
class JobAdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')