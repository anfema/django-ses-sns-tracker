from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from django_ses.views import handle_bounce


urlpatterns = [
    url(r'^bounce/$', csrf_exempt(handle_bounce)),
]
