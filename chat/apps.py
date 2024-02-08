from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    
    # adding signals for pre-save or post-save methods
    def ready(self):
        import chat.signals 
