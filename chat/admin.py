from django.contrib import admin
from . import models

class MessageInline(admin.TabularInline):  # You can also use StackedInline
    model = models.Message
    extra = 0  # Set to 0 to avoid showing empty form fields
    ordering = ('created_at',)

@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('name', 'user1', 'user2',)
    inlines = [MessageInline]  # Add the MessageInline to the ThreadAdmin

# ==================================================================

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id',  'content')

# ==================================================================

@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'reporter', 'date_reported',)
    ordering = ('-id',)