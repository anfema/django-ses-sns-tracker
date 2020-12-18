from django.dispatch import Signal, receiver
from django.utils import timezone

from django_ses.signals import bounce_received, complaint_received, delivery_received

from .models import SESMailDelivery


# our signals
recipients_bounce = Signal(providing_args=['recipients', 'bounce_obj'])
recipients_complaint = Signal(providing_args=['recipients', 'complaint_obj'])
recipients_delivery = Signal(providing_args=['recipients', 'delivery_obj'])


# handle django-ses signals

@receiver(bounce_received)
def bounce_handler(sender, mail_obj, bounce_obj, raw_message, **kwargs):
    recipients = [r['emailAddress'] for r in bounce_obj['bouncedRecipients']]
    SESMailDelivery.objects.filter(message_id=mail_obj['messageId'], recipient__in=recipients).update(
        state=SESMailDelivery.STATE_BOUNCED,
        state_data=bounce_obj,
        mail_data=mail_obj,
        updated_at=timezone.now(),
    )
    recipients_bounce.send(__name__, recipients=recipients, bounce_obj=bounce_obj)


@receiver(complaint_received)
def complaint_handler(sender, mail_obj, complaint_obj, raw_message, **kwargs):
    recipients = [r['emailAddress'] for r in complaint_obj['complainedRecipients']]
    SESMailDelivery.objects.filter(message_id=mail_obj['messageId'], recipient__in=recipients).update(
        state=SESMailDelivery.STATE_COMPLAINT,
        state_data=complaint_obj,
        mail_data=mail_obj,
        updated_at=timezone.now(),
    )
    recipients_complaint.send(__name__, recipients=recipients, complaint_obj=complaint_obj)


@receiver(delivery_received)
def delivery_handler(sender, mail_obj, delivery_obj, raw_message, **kwargs):
    recipients = delivery_obj['recipients']
    SESMailDelivery.objects.filter(message_id=mail_obj['messageId'], recipient__in=recipients).update(
        state=SESMailDelivery.STATE_DELIVERED,
        state_data=delivery_obj,
        mail_data=mail_obj,
        updated_at=timezone.now(),
    )
    recipients_delivery.send(__name__, recipients=recipients, delivery_obj=delivery_obj)
