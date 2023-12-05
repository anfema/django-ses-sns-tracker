from django.urls import path

from django_ses.views import SESEventWebhookView


urlpatterns = [
    path("ses/bounce/", SESEventWebhookView.as_view(), name="handle-event-webhook"),
]
