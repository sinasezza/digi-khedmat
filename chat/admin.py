from django.contrib import admin
from .models import Message, Thread

class MessageInline(admin.TabularInline):  # You can also use StackedInline
    model = Message
    extra = 0  # Set to 0 to avoid showing empty form fields

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2',)
    inlines = [MessageInline]  # Add the MessageInline to the ThreadAdmin

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id',  'content')
