from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ses_sns_tracker", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sesmaildelivery",
            options={"verbose_name": "SES Mail Delivery", "verbose_name_plural": "SES Mail Deliveries"},
        ),
    ]
