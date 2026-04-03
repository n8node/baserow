from datetime import datetime, timezone
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from baserow.contrib.billing.exceptions import (
    CannotDeleteDefaultPlanError,
    CannotDeletePlanWithSubscriptionsError,
    InvalidPlanChangeError,
    PaymentProviderNotActiveError,
    PaymentProviderNotConfiguredError,
    PlanNotFoundError,
    SubscriptionNotFoundError,
)
from baserow.contrib.billing.models import (
    Payment,
    PaymentProviderConfig,
    Plan,
    Subscription,
)

User = get_user_model()


class BillingHandler:
    @staticmethod
    def get_default_plan() -> Plan:
        try:
            return Plan.objects.get(is_default=True, is_active=True)
        except Plan.DoesNotExist:
            raise PlanNotFoundError("No default plan configured.")

    @staticmethod
    def get_plan(plan_id: int) -> Plan:
        try:
            return Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            raise PlanNotFoundError(f"Plan {plan_id} not found.")

    @staticmethod
    def get_plan_by_slug(slug: str) -> Plan:
        try:
            return Plan.objects.get(slug=slug)
        except Plan.DoesNotExist:
            raise PlanNotFoundError(f"Plan '{slug}' not found.")

    @staticmethod
    def get_active_plans() -> QuerySet:
        return Plan.objects.filter(is_active=True).order_by("order")

    @staticmethod
    def get_all_plans() -> QuerySet:
        return Plan.objects.all().order_by("order")

    @staticmethod
    @transaction.atomic
    def create_plan(**kwargs) -> Plan:
        is_default = kwargs.pop("is_default", False)
        plan = Plan.objects.create(**kwargs)
        if is_default:
            Plan.objects.exclude(pk=plan.pk).update(is_default=False)
            plan.is_default = True
            plan.save(update_fields=["is_default"])
        return plan

    @staticmethod
    @transaction.atomic
    def update_plan(plan_id: int, **kwargs) -> Plan:
        plan = BillingHandler.get_plan(plan_id)
        is_default = kwargs.pop("is_default", None)

        for key, value in kwargs.items():
            if hasattr(plan, key):
                setattr(plan, key, value)
        plan.save()

        if is_default is True:
            Plan.objects.exclude(pk=plan.pk).update(is_default=False)
            plan.is_default = True
            plan.save(update_fields=["is_default"])
        elif is_default is False:
            plan.is_default = False
            plan.save(update_fields=["is_default"])

        return plan

    @staticmethod
    @transaction.atomic
    def delete_plan(plan_id: int):
        plan = BillingHandler.get_plan(plan_id)
        if plan.is_default:
            raise CannotDeleteDefaultPlanError(
                "Cannot delete the default plan. Set another plan as default first."
            )
        if plan.subscriptions.exists():
            raise CannotDeletePlanWithSubscriptionsError(
                "Cannot delete a plan with active subscriptions. "
                "Migrate subscribers first."
            )
        plan.delete()

    @staticmethod
    @transaction.atomic
    def create_default_subscription(user) -> Subscription:
        if hasattr(user, "subscription"):
            return user.subscription

        try:
            default_plan = BillingHandler.get_default_plan()
        except PlanNotFoundError:
            return None

        return Subscription.objects.create(
            user=user,
            plan=default_plan,
            status=Subscription.Status.ACTIVE,
            current_period_start=datetime.now(tz=timezone.utc),
        )

    @staticmethod
    def get_subscription(user) -> Subscription:
        try:
            return Subscription.objects.select_related("plan").get(user=user)
        except Subscription.DoesNotExist:
            raise SubscriptionNotFoundError(
                f"No subscription found for user {user.email}"
            )

    @staticmethod
    def get_subscription_safe(user) -> Optional[Subscription]:
        try:
            return Subscription.objects.select_related("plan").get(user=user)
        except Subscription.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def change_plan(user, new_plan_id: int) -> Subscription:
        new_plan = BillingHandler.get_plan(new_plan_id)
        if not new_plan.is_active:
            raise InvalidPlanChangeError("Target plan is not active.")

        sub = BillingHandler.get_subscription(user)
        old_plan = sub.plan

        if old_plan.pk == new_plan.pk:
            raise InvalidPlanChangeError("Already on this plan.")

        sub.plan = new_plan
        sub.updated_at = datetime.now(tz=timezone.utc)
        sub.save(update_fields=["plan", "updated_at"])
        return sub

    @staticmethod
    def get_active_provider() -> PaymentProviderConfig:
        try:
            return PaymentProviderConfig.objects.get(is_active=True)
        except PaymentProviderConfig.DoesNotExist:
            raise PaymentProviderNotActiveError("No active payment provider.")

    @staticmethod
    def get_provider(provider_type: str) -> PaymentProviderConfig:
        try:
            return PaymentProviderConfig.objects.get(provider_type=provider_type)
        except PaymentProviderConfig.DoesNotExist:
            raise PaymentProviderNotConfiguredError(
                f"Provider '{provider_type}' not configured."
            )

    @staticmethod
    def get_all_providers() -> QuerySet:
        return PaymentProviderConfig.objects.all()

    @staticmethod
    @transaction.atomic
    def update_provider(provider_type: str, **kwargs) -> PaymentProviderConfig:
        config, _ = PaymentProviderConfig.objects.get_or_create(
            provider_type=provider_type
        )
        for key, value in kwargs.items():
            if hasattr(config, key) and key != "provider_type":
                setattr(config, key, value)
        config.save()
        return config

    @staticmethod
    @transaction.atomic
    def activate_provider(provider_type: str) -> PaymentProviderConfig:
        PaymentProviderConfig.objects.filter(is_active=True).update(is_active=False)
        config, _ = PaymentProviderConfig.objects.get_or_create(
            provider_type=provider_type
        )
        config.is_active = True
        config.save(update_fields=["is_active"])
        return config

    @staticmethod
    @transaction.atomic
    def deactivate_provider(provider_type: str) -> PaymentProviderConfig:
        config = BillingHandler.get_provider(provider_type)
        config.is_active = False
        config.save(update_fields=["is_active"])
        return config

    @staticmethod
    @transaction.atomic
    def record_payment(
        subscription: Subscription,
        amount,
        provider: str,
        external_id: str = "",
        status: str = Payment.Status.PENDING,
        description: str = "",
        metadata: dict = None,
    ) -> Payment:
        return Payment.objects.create(
            subscription=subscription,
            amount=amount,
            currency=subscription.plan.currency,
            status=status,
            payment_provider=provider,
            external_payment_id=external_id,
            description=description,
            metadata=metadata or {},
        )

    @staticmethod
    def confirm_payment(payment_id: int) -> Payment:
        payment = Payment.objects.get(pk=payment_id)
        payment.status = Payment.Status.SUCCEEDED
        payment.paid_at = datetime.now(tz=timezone.utc)
        payment.save(update_fields=["status", "paid_at"])

        sub = payment.subscription
        if sub.status != Subscription.Status.ACTIVE:
            sub.status = Subscription.Status.ACTIVE
            sub.save(update_fields=["status"])

        return payment

    @staticmethod
    def user_has_feature(user, feature: str) -> bool:
        sub = BillingHandler.get_subscription_safe(user)
        if sub and sub.is_usable:
            return feature in (sub.plan.features or [])
        return False

    @staticmethod
    def get_user_plan_features(user) -> list:
        sub = BillingHandler.get_subscription_safe(user)
        if sub and sub.is_usable:
            return sub.plan.features or []
        return []
