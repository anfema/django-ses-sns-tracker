from django.urls import path

from .views import SESSNSTrackerWebhookView


"""
URLConf left for compatibility. New setups should use the view directly in their own URLConf.
"""

app_name = 'ses_sns_tracker'

urlpatterns = [
    path('bounce/', SESSNSTrackerWebhookView.as_view(), name='handle-event-webhook'),
]
