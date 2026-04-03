from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Plan(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="RUB")

    max_rows_per_workspace = models.IntegerField(
        null=True,
        blank=True,
        help_text="NULL means unlimited.",
    )
    max_storage_mb = models.IntegerField(null=True, blank=True)
    max_workspaces = models.IntegerField(null=True, blank=True)
    max_collaborators_per_workspace = models.IntegerField(null=True, blank=True)
    max_automations = models.IntegerField(null=True, blank=True)
    max_api_calls_per_month = models.IntegerField(null=True, blank=True)
    max_file_upload_size_mb = models.IntegerField(null=True, blank=True)

    features = models.JSONField(
        default=list,
        blank=True,
        help_text='List of feature slugs, e.g. ["premium","row_comments"]',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["is_default"],
                condition=models.Q(is_default=True),
                name="billing_only_one_default_plan",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.slug})"


class PaymentProviderConfig(models.Model):
    class ProviderType(models.TextChoices):
        ROBOKASSA = "robokassa", "Робокасса"
        YOOKASSA = "yookassa", "ЮKassa"

    provider_type = models.CharField(
        max_length=20, choices=ProviderType.choices, unique=True
    )
    is_active = models.BooleanField(default=False)

    merchant_login = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Robokassa: MerchantLogin",
    )
    password1 = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Robokassa: Password #1",
    )
    password2 = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Robokassa: Password #2",
    )

    shop_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="YooKassa: Shop ID",
    )
    secret_key = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="YooKassa: Secret key",
    )

    test_mode = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=models.Q(is_active=True),
                name="billing_only_one_active_provider",
            )
        ]

    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"{self.get_provider_type_display()} ({status})"


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAST_DUE = "past_due", "Past due"
        CANCELLED = "cancelled", "Cancelled"
        TRIAL = "trial", "Trial"
        EXPIRED = "expired", "Expired"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, related_name="subscriptions"
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    payment_provider = models.CharField(max_length=20, blank=True, default="")
    external_subscription_id = models.CharField(max_length=255, blank=True, default="")

    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_usable(self):
        return self.status in (self.Status.ACTIVE, self.Status.TRIAL)

    def __str__(self):
        return f"{self.user.email} → {self.plan.name} ({self.status})"


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="RUB")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    payment_provider = models.CharField(max_length=20)
    external_payment_id = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")

    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment #{self.pk} — {self.amount} {self.currency} ({self.status})"
