from django.conf import settings


default_app_config = 'ses_sns_tracker.apps.SESSNSTrackerConfig'


if getattr(settings, 'SES_SNS_TRACKER_USE_CRYPTOGRAPHY', True):
    # monkey patch django_ses.utils.verify_bounce_message (to use CryptographyBounceMessageVerifier)
    import django_ses.utils

    from .utils import verify_bounce_message
    django_ses.utils.verify_bounce_message = verify_bounce_message
