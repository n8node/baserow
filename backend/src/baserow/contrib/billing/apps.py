from django.apps import AppConfig


class BillingConfig(AppConfig):
    name = "baserow.contrib.billing"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from baserow.api.registries import RegisteredException, api_exception_registry
        from baserow.api.user.registries import (
            member_data_registry,
            user_data_registry,
        )
        from baserow.contrib.database.rows.signals import before_rows_create
        from baserow.core.registries import plugin_registry

        from .exceptions import PlanLimitExceededError
        from .limits import on_before_rows_create
        from .member_data_types import BillingPlanMemberDataType
        from .plugin import BillingPlugin
        from .user_data_types import SubscriptionDataType

        plugin_registry.register(BillingPlugin())
        user_data_registry.register(SubscriptionDataType())
        member_data_registry.register(BillingPlanMemberDataType())

        before_rows_create.connect(on_before_rows_create)

        api_exception_registry.register(
            RegisteredException(
                exception_class=PlanLimitExceededError,
                exception_error=(
                    "ERROR_BILLING_PLAN_LIMIT_EXCEEDED",
                    402,
                    "{e}",
                ),
            )
        )
