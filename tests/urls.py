from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from django_ses.views import handle_bounce


urlpatterns = [
    path('ses/bounce/', csrf_exempt(handle_bounce), name='django_ses_bounce'),
]
