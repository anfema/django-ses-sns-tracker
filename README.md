# django-ses-sns-tracker
A simple wrapper around django-ses to receive and persist sns event data.

Records mail delivery in the `SESMailDelivery` model and updates the state if a matching SNS notification is received.


## Requirements

- [Django](https://www.djangoproject.com) version 3.2+
- A [PostgreSQL](https://www.postgresql.org/) Database


## Quick start

1. Add `ses_sns_tracker` to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        # ...
        'ses_sns_tracker',
    ]
    ```

2. Run `python manage.py migrate` to create the models.

3. [Setup](https://github.com/django-ses/django-ses#full-list-of-settings) `django-ses`

4. Add the webhook view to `urls.py`:

    ```python
    from django_ses.views import SESEventWebhookView

    urlpatterns = [
        # ...
        path('ses-events/', SESEventWebhookView.as_view(), name='handle-event-webhook'),
        # ...
    ]
    ```

5. (Optional) Use `ses_sns_tracker.backends.SESSNSTrackerBackend` as your default email backend:

    ```
    EMAIL_BACKEND = 'ses_sns_tracker.backends.SESSNSTrackerBackend'
    ```

    This way all emails will be sent via the Amazon SES API.

6. (Optional) Send an email via the `SESMailDelivery` manager (doesn't require `SESSNSTrackerBackend`
    as the default mail backend):

    ```python
    from django.core.mail import EmailMessage
    from ses_sns_tracker.models import SESMailDelivery

    message = EmailMessage(
        subject='email subject',
        body='email body',
        from_email='sender@example.com',
        to=['recipient@example.com'],
    )
    SESMailDelivery.objects.create_message(message, fail_silently=False, fake_delivery=False)
    ```


## Settings

- `SES_SNS_TRACKER_DEBUG_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

    Set mail backend to use for the actual mail delivery in `DEBUG` mode (`SESMailDelivery` objects
    will still be created).
    *Default: `None`*


## Development setup

1. Upgrade packaging tools:

    ```bash
    pip install --upgrade pip setuptools wheel
    ```

2. Install development dependencies:

    ```bash
    poetry install
    ```

3. (Optional) Override settings in `example_proj/settings_local.py` & `tests/settings_local.py` as required.
