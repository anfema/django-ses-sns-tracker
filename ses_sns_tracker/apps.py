from django.apps import AppConfig


class SESSNSTrackerConfig(AppConfig):
    name = 'ses_sns_tracker'
    verbose_name = "SES/SNS Tracker"
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from . import signals  # NOQA
