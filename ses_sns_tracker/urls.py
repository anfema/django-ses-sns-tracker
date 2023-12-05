from django.urls import path

from django_ses.views import SESEventWebhookView


"""
URLConf left for compatibility. New setups should use the view directly in their own URLConf.
"""

app_name = 'ses_sns_tracker'

urlpatterns = [
    path('bounce/', SESEventWebhookView.as_view(), name='handle-event-webhook'),
]
