from django.core.mail import EmailMessage
from django.test import TestCase

from ses_sns_tracker.models import SESMailDelivery


class FakeDeliveryTestCase(TestCase):
    def test_fake_delivery(self):
        message = EmailMessage(
            subject="test message",
            body="mail content",
            from_email="sender@local",
            to=["recipient@local"],
        )

        SESMailDelivery.objects.create_message(message, fail_silently=False, fake_delivery=True)

        self.assertTrue(SESMailDelivery.objects.filter(recipient="recipient@local").exists())
