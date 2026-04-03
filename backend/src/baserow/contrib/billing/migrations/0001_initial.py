import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, default="")),
                ("is_default", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "price_monthly",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "price_yearly",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("currency", models.CharField(default="RUB", max_length=3)),
                (
                    "max_rows_per_workspace",
                    models.IntegerField(
                        blank=True, help_text="NULL means unlimited.", null=True
                    ),
                ),
                ("max_storage_mb", models.IntegerField(blank=True, null=True)),
                ("max_workspaces", models.IntegerField(blank=True, null=True)),
                (
                    "max_collaborators_per_workspace",
                    models.IntegerField(blank=True, null=True),
                ),
                ("max_automations", models.IntegerField(blank=True, null=True)),
                ("max_api_calls_per_month", models.IntegerField(blank=True, null=True)),
                ("max_file_upload_size_mb", models.IntegerField(blank=True, null=True)),
                (
                    "features",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text='List of feature slugs, e.g. ["premium","row_comments"]',
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.AddConstraint(
            model_name="plan",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_default", True)),
                fields=("is_default",),
                name="billing_only_one_default_plan",
            ),
        ),
        migrations.CreateModel(
            name="PaymentProviderConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "provider_type",
                    models.CharField(
                        choices=[
                            ("robokassa", "Робокасса"),
                            ("yookassa", "ЮKassa"),
                        ],
                        max_length=20,
                        unique=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "merchant_login",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Robokassa: MerchantLogin",
                        max_length=255,
                    ),
                ),
                (
                    "password1",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Robokassa: Password #1",
                        max_length=255,
                    ),
                ),
                (
                    "password2",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Robokassa: Password #2",
                        max_length=255,
                    ),
                ),
                (
                    "shop_id",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="YooKassa: Shop ID",
                        max_length=255,
                    ),
                ),
                (
                    "secret_key",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="YooKassa: Secret key",
                        max_length=255,
                    ),
                ),
                ("test_mode", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name="paymentproviderconfig",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("is_active",),
                name="billing_only_one_active_provider",
            ),
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("past_due", "Past due"),
                            ("cancelled", "Cancelled"),
                            ("trial", "Trial"),
                            ("expired", "Expired"),
                        ],
                        default="active",
                        max_length=20,
                    ),
                ),
                (
                    "payment_provider",
                    models.CharField(blank=True, default="", max_length=20),
                ),
                (
                    "external_subscription_id",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "current_period_start",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "current_period_end",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("trial_end", models.DateTimeField(blank=True, null=True)),
                ("cancelled_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="subscriptions",
                        to="billing.plan",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscription",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(default="RUB", max_length=3)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("succeeded", "Succeeded"),
                            ("failed", "Failed"),
                            ("refunded", "Refunded"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("payment_provider", models.CharField(max_length=20)),
                (
                    "external_payment_id",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("description", models.TextField(blank=True, default="")),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "subscription",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="billing.subscription",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
