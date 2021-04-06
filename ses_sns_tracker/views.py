from django.conf import settings

from django_ses.views import SESEventWebhookView

from .utils import cryptography_verify_event_message


class SESSNSTrackerWebhookView(SESEventWebhookView):
    def verify_event_message(self, notification):
        if getattr(settings, 'SES_SNS_TRACKER_USE_CRYPTOGRAPHY', True):
            return cryptography_verify_event_message(notification)
        return super().verify_event_message(notification)
