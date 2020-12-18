# django-ses-sns-tracker
A simple wrapper around django-ses to receive and persist sns event data.

Records mail delivery in the `SESMailDelivery` model and updates the state if a matching SNS notification is received.


## Requirements

- [Django](https://www.djangoproject.com) version 2.2+
- A [PostgreSQL](https://www.postgresql.org/) Database


## Quick start

1. Add `ses_sns_tracker` to your INSTALLED_APPS setting like this:

    ```
    INSTALLED_APPS = [
        ...
        'ses_sns_tracker',
    ]
    ```

2. Run `python manage.py migrate` to create the models.

3. [Setup](https://github.com/django-ses/django-ses#full-list-of-settings) `django-ses`

4. (Optional) Use `ses_sns_tracker.backends.SESSNSTrackerBackend` as your default email backend:

    ```
    EMAIL_BACKEND = 'ses_sns_tracker.backends.SESSNSTrackerBackend'
    ```

    This way all emails will be send via the Amazon SES API.

5. (Optional) Send an email via the `SESMailDelivery` manager (doesn't require `SESSNSTrackerBackend`
    as the default mail backend):

    ```python
    from django.core.mail import EmailMessage
    from ses_sns_tracker.models import SESMailDelivery

    message = EmailMessage(
        subject='email subject',
        body='email body',
        from_email='from@example.org',
        to=['recipient@example.org'],
    )
    SESMailDelivery.objects.create_message(message, fail_silently=False, fake_delivery=False)
    ```


## Settings

- `SES_SNS_TRACKER_DEBUG_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

    Set mail backend to use for the actual mail delivery in `DEBUG` mode (`SESMailDelivery` objects
    will still be created).
    *Default: `None`*

- `SES_SNS_TRACKER_USE_CRYPTOGRAPHY = True`

    Use `crypthography` instead of `M2Crypto` to verify the signature of messages received from SNS.
    *Default: `True`*


## Development setup

1. Upgrade packaging tools:

    ```bash
    pip install --upgrade pip setuptools wheel
    ```

2. Install packages from `requirements-dev.txt`:

    ```bash
    pip install -r requirements-dev.txt
    ```

3. (Optional) Override settings in `example_proj/settings_local.py` & `tests/settings_local.py` as required.
