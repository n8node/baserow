from django.apps import AppConfig


class BillingConfig(AppConfig):
    name = "baserow.contrib.billing"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from baserow.api.user.registries import user_data_registry
        from baserow.core.registries import plugin_registry

        from .plugin import BillingPlugin
        from .user_data_types import SubscriptionDataType

        plugin_registry.register(BillingPlugin())
        user_data_registry.register(SubscriptionDataType())
