from django.apps import AppConfig


class SESSNSTrackerConfig(AppConfig):
    name = 'ses_sns_tracker'
    verbose_name = "SES/SNS Tracker"

    def ready(self):
        from . import signals  # NOQA
