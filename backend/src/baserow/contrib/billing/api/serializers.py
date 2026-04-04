from rest_framework import serializers

from baserow.contrib.billing.models import (
    Payment,
    PaymentProviderConfig,
    Plan,
    Subscription,
)


class PlanSerializer(serializers.ModelSerializer):
    subscription_count = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "slug",
            "name",
            "description",
            "is_default",
            "is_active",
            "order",
            "price_monthly",
            "price_yearly",
            "currency",
            "max_rows_per_workspace",
            "max_storage_mb",
            "max_workspaces",
            "max_collaborators_per_workspace",
            "max_automations",
            "max_api_calls_per_month",
            "max_file_upload_size_mb",
            "features",
            "subscription_count",
        ]

    def get_subscription_count(self, obj):
        annotated = getattr(obj, "subscription_count", None)
        if annotated is not None:
            return annotated
        return obj.subscriptions.count()


class PlanPublicSerializer(serializers.ModelSerializer):
    """Subset of fields visible to non-admin users."""

    class Meta:
        model = Plan
        fields = [
            "id",
            "slug",
            "name",
            "description",
            "order",
            "price_monthly",
            "price_yearly",
            "currency",
            "max_rows_per_workspace",
            "max_storage_mb",
            "max_workspaces",
            "max_collaborators_per_workspace",
            "max_automations",
            "max_api_calls_per_month",
            "max_file_upload_size_mb",
            "features",
        ]


class CreatePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "slug",
            "name",
            "description",
            "is_default",
            "is_active",
            "order",
            "price_monthly",
            "price_yearly",
            "currency",
            "max_rows_per_workspace",
            "max_storage_mb",
            "max_workspaces",
            "max_collaborators_per_workspace",
            "max_automations",
            "max_api_calls_per_month",
            "max_file_upload_size_mb",
            "features",
        ]


_UPDATE_PLAN_FIELDS = [
    "slug",
    "name",
    "description",
    "is_default",
    "is_active",
    "order",
    "price_monthly",
    "price_yearly",
    "currency",
    "max_rows_per_workspace",
    "max_storage_mb",
    "max_workspaces",
    "max_collaborators_per_workspace",
    "max_automations",
    "max_api_calls_per_month",
    "max_file_upload_size_mb",
    "features",
]


class UpdatePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = _UPDATE_PLAN_FIELDS
        extra_kwargs = {f: {"required": False} for f in _UPDATE_PLAN_FIELDS}


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "plan",
            "plan_id",
            "status",
            "payment_provider",
            "current_period_start",
            "current_period_end",
            "trial_end",
            "cancelled_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "payment_provider",
            "current_period_start",
            "current_period_end",
            "trial_end",
            "cancelled_at",
            "created_at",
            "updated_at",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "currency",
            "status",
            "payment_provider",
            "description",
            "paid_at",
            "created_at",
        ]


class SubscribeRequestSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    billing_period = serializers.ChoiceField(
        choices=["monthly", "yearly"], default="monthly"
    )


class PaymentProviderConfigSerializer(serializers.ModelSerializer):
    password1 = serializers.SerializerMethodField()
    password2 = serializers.SerializerMethodField()
    secret_key = serializers.SerializerMethodField()

    class Meta:
        model = PaymentProviderConfig
        fields = [
            "id",
            "provider_type",
            "is_active",
            "merchant_login",
            "password1",
            "password2",
            "shop_id",
            "secret_key",
            "test_mode",
        ]

    def _mask(self, value: str) -> str:
        if not value:
            return ""
        if len(value) <= 4:
            return "****"
        return "****" + value[-4:]

    def get_password1(self, obj):
        return self._mask(obj.password1)

    def get_password2(self, obj):
        return self._mask(obj.password2)

    def get_secret_key(self, obj):
        return self._mask(obj.secret_key)


class UpdatePaymentProviderSerializer(serializers.Serializer):
    merchant_login = serializers.CharField(required=False, allow_blank=True)
    password1 = serializers.CharField(required=False, allow_blank=True)
    password2 = serializers.CharField(required=False, allow_blank=True)
    shop_id = serializers.CharField(required=False, allow_blank=True)
    secret_key = serializers.CharField(required=False, allow_blank=True)
    test_mode = serializers.BooleanField(required=False)
