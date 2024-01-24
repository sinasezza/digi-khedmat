from django.contrib import admin
from . import models


@admin.register(models.Advertise)
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')