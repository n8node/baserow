from baserow.api.user.registries import UserDataType


class SubscriptionDataType(UserDataType):
    type = "subscription"

    def get_user_data(self, user, request) -> dict:
        from baserow.contrib.billing.handler import BillingHandler

        sub = BillingHandler.get_subscription_safe(user)
        if sub and sub.is_usable:
            plan = sub.plan
            return {
                "plan_slug": plan.slug,
                "plan_name": plan.name,
                "plan_id": plan.id,
                "status": sub.status,
                "features": plan.features or [],
                "limits": {
                    "max_rows_per_workspace": plan.max_rows_per_workspace,
                    "max_storage_mb": plan.max_storage_mb,
                    "max_workspaces": plan.max_workspaces,
                    "max_collaborators_per_workspace": plan.max_collaborators_per_workspace,
                    "max_automations": plan.max_automations,
                    "max_api_calls_per_month": plan.max_api_calls_per_month,
                    "max_file_upload_size_mb": plan.max_file_upload_size_mb,
                },
                "current_period_end": (
                    sub.current_period_end.isoformat()
                    if sub.current_period_end
                    else None
                ),
            }
        return {
            "plan_slug": "free",
            "plan_name": "Free",
            "plan_id": None,
            "status": "none",
            "features": [],
            "limits": {},
            "current_period_end": None,
        }
