from typing import List, Optional

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.mail import EmailMessage
from django.db import models
from django.utils.module_loading import import_string

from django_ses import SESBackend


class SESMailManager(models.Manager):
    def create_message(self, message, fail_silently=False):
        # type: (EmailMessage, bool) -> List[SESMailDelivery]
        assert isinstance(message, EmailMessage)
        assert message.connection is None or isinstance(message.connection, SESBackend)

        if settings.DEBUG and getattr(settings, 'SES_SNS_TRACKER_DEBUG_BACKEND', None):
            debug_backend = import_string(settings.SES_SNS_TRACKER_DEBUG_BACKEND)
            message.connection = debug_backend()
        elif message.connection is None:
            message.connection = SESBackend()

        message.send(fail_silently=fail_silently)
        deliveries = list()
        for recipient in message.recipients():
            deliveries.append(self.model(
                recipient=recipient,
                message_id=message.extra_headers.get('message_id', 'NO_MESSAGE_ID'),
                request_id=message.extra_headers.get('request_id', 'NO_RESULT_ID'),
            ))
        return self.bulk_create(deliveries)


class SESMailDelivery(models.Model):
    STATE_SENT = 0
    STATE_DELIVERED = 1
    STATE_BOUNCED = 2
    STATE_COMPLAINT = 3
    DELIVERY_STATES = (
        (STATE_SENT, 'Sent'),
        (STATE_DELIVERED, 'Delivered'),
        (STATE_BOUNCED, 'Bounced'),
        (STATE_COMPLAINT, 'Complaint'),
    )

    recipient = models.EmailField()
    message_id = models.CharField(max_length=128)
    request_id = models.CharField(max_length=128)
    state = models.PositiveSmallIntegerField(choices=DELIVERY_STATES, default=0)
    state_data = JSONField(
        default=dict, blank=True,
        help_text='Amazon SNS event data (bounce/complaint/delivery object)',
    )
    mail_data = JSONField(default=dict, help_text='Amazon SNS mail data', blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SESMailManager()

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = 'SES Mail Delivery'
        verbose_name_plural = 'SES Mail Deliveries'

    def __str__(self):
        return '{} ({} {})'.format(self.recipient, self.get_state_display(), self.updated_at)

    @property
    def success(self):
        # type: () -> Optional[bool]
        if self.state == self.STATE_SENT:
            return None
        return self.state == self.STATE_DELIVERED

    @property
    def error_reason(self):
        # type: () -> Optional[str]
        if self.state == self.STATE_BOUNCED:
            return self._bounce_reason()
        if self.state == self.STATE_COMPLAINT:
            return self._complaint_reason()

    def _bounce_reason(self):
        # type: () -> str
        return '{}.{}'.format(self.state_data.get('bounceType'), self.state_data.get('bounceSubType'))

    def _complaint_reason(self):
        # type: () -> str
        return self.state_data.get('complaintFeedbackType')
