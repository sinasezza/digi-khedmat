from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number',)

# =================================================================

@admin.register(models.NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# =================================================================

# @admin.register(models.Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('recipient', 'notification_type',)