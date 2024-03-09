from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    # adding signals for pre-save or post-save methods
    def ready(self):
        import jobs.signals