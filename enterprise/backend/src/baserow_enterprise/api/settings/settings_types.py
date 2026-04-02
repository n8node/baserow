from django.conf import settings
from django.http import HttpRequest

from baserow.api.settings.registries import SettingsDataType


class EnterpriseUnlicensedFeaturesSettingsDataType(SettingsDataType):
    """
    Exposes fork-only flags to the web frontend so Enterprise UI (SSO, audit log,
    data scanner, branding) can enable without relying on Nuxt env → runtimeConfig.
    """

    type = "enterprise_unlicensed_features"

    def get_settings_data(self, request: HttpRequest) -> dict:
        enabled = getattr(settings, "BASEROW_ENTERPRISE_FORK_UNLICENSED", False) or getattr(
            settings, "BASEROW_ENTERPRISE_SSO_AUDIT_LOG_UNLICENSED", False
        )
        return {
            "enabled": enabled,
            "sso_audit_log_enabled": enabled,
        }
