from django.urls import path

from ses_sns_tracker.views import SESSNSTrackerWebhookView


urlpatterns = [
    path('ses/bounce/', SESSNSTrackerWebhookView.as_view(), name='handle-event-webhook'),
]
