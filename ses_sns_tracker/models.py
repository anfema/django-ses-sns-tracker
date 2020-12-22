from typing import Optional

from django.contrib.postgres.fields import JSONField
from django.db import models

from .managers import SESMailManager


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
    state = models.PositiveSmallIntegerField(choices=DELIVERY_STATES, default=STATE_SENT)
    state_data = JSONField(
        default=dict, blank=True,
        help_text='Amazon SNS event data (bounce/complaint/delivery object)',
    )
    mail_data = JSONField(default=dict, help_text='Amazon SNS mail data', blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SESMailManager()

    class Meta:
        verbose_name = 'SES Mail Delivery'
        verbose_name_plural = 'SES Mail Deliveries'

    def __str__(self):
        return f'{self.recipient} ({self.get_state_display()} {self.updated_at})'

    @property
    def success(self) -> Optional[bool]:
        if self.state == self.STATE_SENT:
            return None
        return self.state == self.STATE_DELIVERED

    @property
    def error_reason(self) -> Optional[str]:
        if self.state == self.STATE_BOUNCED:
            return self._bounce_reason()
        if self.state == self.STATE_COMPLAINT:
            return self._complaint_reason()

    def _bounce_reason(self) -> str:
        return f'{self.state_data.get("bounceType")}.{self.state_data.get("bounceSubType")}'

    def _complaint_reason(self) -> str:
        return self.state_data.get('complaintFeedbackType')
