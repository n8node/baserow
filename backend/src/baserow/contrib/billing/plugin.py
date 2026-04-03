from django.urls import include, path

from baserow.core.registries import Plugin


class BillingPlugin(Plugin):
    type = "billing"

    def get_api_urls(self):
        from baserow.contrib.billing.api import urls as api_urls

        return [
            path("billing/", include(api_urls, namespace=self.type)),
        ]

    def user_created(self, user, workspace=None, workspace_invitation=None, template=None):
        from baserow.contrib.billing.handler import BillingHandler

        try:
            BillingHandler.create_default_subscription(user)
        except Exception:
            pass
