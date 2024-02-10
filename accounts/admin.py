from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number',)

# =================================================================

@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'recipient', 'seen', 'date_created',)

# =================================================================

@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'content_object', 'owner',)