from django.conf import settings

from baserow.api.settings.registries import SettingsDataType
from baserow.core.registries import plugin_registry


class InstanceWideSettingsDataType(SettingsDataType):
    type = "instance_wide_licenses"

    def get_settings_data(self, request):
        """
        Someone who authenticates via the API should know beforehand if the related
        user has active licenses.
        """

        from baserow_premium.plugins import PremiumPlugin

        license_plugin = plugin_registry.get_by_type(PremiumPlugin).get_license_plugin()

        instance_wide_licenses = {
            license_type.type: True
            for license_type in license_plugin.get_active_instance_wide_license_types(
                None
            )
        }
        if getattr(settings, "BASEROW_PREMIUM_FEATURES_UNLICENSED", False) or getattr(
            settings, "BASEROW_ENTERPRISE_FORK_UNLICENSED", False
        ) or getattr(settings, "BASEROW_ENTERPRISE_SSO_AUDIT_LOG_UNLICENSED", False):
            instance_wide_licenses["premium"] = True
        return instance_wide_licenses
