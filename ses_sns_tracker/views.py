from django_ses.views import SESEventWebhookView
from typing_extensions import deprecated


@deprecated("Use SESEventWebhookView instead")
class SESSNSTrackerWebhookView(SESEventWebhookView):
    """Deprecated. Use SESEventWebhookView directly instead."""
