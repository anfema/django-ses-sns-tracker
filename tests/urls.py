from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from django_ses.views import handle_bounce


urlpatterns = [
    url(r'^ses/bounce/$', csrf_exempt(handle_bounce), name='django_ses_bounce'),
]
