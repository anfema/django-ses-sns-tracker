from django.conf import settings
from django.utils.module_loading import import_string

from django_ses import SESBackend

from .models import SESMailDelivery


class SESSNSTrackerBackend(SESBackend):
    def send_messages(self, email_messages) -> int:
        if settings.DEBUG and getattr(settings, 'SES_SNS_TRACKER_DEBUG_BACKEND', None):
            debug_backend = import_string(settings.SES_SNS_TRACKER_DEBUG_BACKEND)
            num_sent = debug_backend().send_messages(email_messages)
        else:
            num_sent = super().send_messages(email_messages)
        deliveries = list()

        for message in email_messages:
            for recipient in message.recipients():
                deliveries.append(SESMailDelivery(
                    recipient=recipient,
                    message_id=message.extra_headers.get('message_id', 'NO_MESSAGE_ID'),
                    request_id=message.extra_headers.get('request_id', 'NO_RESULT_ID'),
                ))

        SESMailDelivery.objects.bulk_create(deliveries)

        return num_sent
