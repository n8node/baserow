from django.conf import settings
from django.http import HttpRequest

from baserow.api.settings.registries import SettingsDataType


class EnterpriseUnlicensedFeaturesSettingsDataType(SettingsDataType):
    """
    Exposes fork-only flags to the web frontend so Enterprise UI (full feature set
    matching a self-hosted Enterprise license) can enable without Nuxt env wiring.
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
