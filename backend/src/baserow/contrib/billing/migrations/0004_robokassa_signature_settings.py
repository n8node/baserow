from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0003_create_subscriptions_for_existing_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentproviderconfig",
            name="fiscalization_enabled",
            field=models.BooleanField(
                default=False,
                help_text="Send Receipt JSON for 54-FZ (must match Robokassa fiscalization).",
            ),
        ),
        migrations.AddField(
            model_name="paymentproviderconfig",
            name="hash_algorithm",
            field=models.CharField(
                blank=True,
                default="md5",
                help_text="Robokassa hash algorithm from merchant technical settings "
                "(md5, sha1, sha256, sha384, sha512).",
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="paymentproviderconfig",
            name="receipt_sno",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional Receipt sno (osn, usn_income, ...). "
                "Empty = cabinet default.",
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name="paymentproviderconfig",
            name="receipt_tax",
            field=models.CharField(
                blank=True,
                default="none",
                help_text="Robokassa Receipt item tax (none, vat0, vat10, vat20, ...).",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="paymentproviderconfig",
            name="test_mode",
            field=models.BooleanField(
                default=True,
                help_text="Robokassa: send IsTest=1. Must use TEST Password #1/#2, "
                "not live passwords (otherwise error 29).",
            ),
        ),
    ]
