from typing import TYPE_CHECKING, List

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.utils.module_loading import import_string

from django_ses import SESBackend


if TYPE_CHECKING:
    from .models import SESMailDelivery


class SESMailManager(models.Manager):
    def create_message(
        self,
        message: EmailMessage,
        fail_silently: bool = False,
        fake_delivery: bool = False,
    ) -> List['SESMailDelivery']:
        assert isinstance(message, EmailMessage)
        assert message.connection is None or isinstance(message.connection, SESBackend)

        if settings.DEBUG and getattr(settings, 'SES_SNS_TRACKER_DEBUG_BACKEND', None):
            debug_backend = import_string(settings.SES_SNS_TRACKER_DEBUG_BACKEND)
            message.connection = debug_backend()
        elif message.connection is None:
            message.connection = SESBackend()

        if not fake_delivery:
            message.send(fail_silently=fail_silently)

        deliveries = list()
        for recipient in message.recipients():
            deliveries.append(self.model(
                recipient=recipient,
                message_id=message.extra_headers.get('message_id', 'NO_MESSAGE_ID'),
                request_id=message.extra_headers.get('request_id', 'NO_RESULT_ID'),
                state=self.model.STATE_DELIVERED if fake_delivery else self.model.SESMailDelivery.STATE_SENT,
            ))
        return self.bulk_create(deliveries)
