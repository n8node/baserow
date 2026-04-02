from django.conf import settings
from django.http import HttpRequest

from baserow.api.settings.registries import SettingsDataType


class EnterpriseUnlicensedFeaturesSettingsDataType(SettingsDataType):
    """
    Exposes fork-only flags to the web frontend so Enterprise UI (e.g. admin SSO /
    audit log) can enable without relying on Nuxt env → runtimeConfig wiring.
    """

    type = "enterprise_unlicensed_features"

    def get_settings_data(self, request: HttpRequest) -> dict:
        return {
            "sso_audit_log_enabled": getattr(
                settings, "BASEROW_ENTERPRISE_SSO_AUDIT_LOG_UNLICENSED", False
            )
        }
