from typing import Dict, List, OrderedDict, Union

from django.contrib.auth.models import AbstractUser

from rest_framework import serializers

from baserow.api.user.registries import MemberDataType
from baserow.contrib.billing.models import Subscription


class BillingPlanMemberDataType(MemberDataType):
    type = "billing_plan"

    def get_request_serializer_field(
        self,
    ) -> Union[serializers.Field, Dict[str, serializers.Field]]:
        return {}

    def annotate_serialized_workspace_members_data(
        self, workspace, serialized_data, user
    ):
        return serialized_data

    def annotate_serialized_admin_users_data(
        self,
        user_ids: List[int],
        serialized_data: List[OrderedDict],
        user: AbstractUser,
    ) -> List[OrderedDict]:
        subs = (
            Subscription.objects.select_related("plan")
            .filter(user_id__in=user_ids)
            .values_list("user_id", "plan__name", "plan__slug", "plan__id")
        )
        plan_map = {
            uid: {"plan_name": name, "plan_slug": slug, "plan_id": pid}
            for uid, name, slug, pid in subs
        }

        for row in serialized_data:
            info = plan_map.get(row["id"], {})
            row["billing_plan_name"] = info.get("plan_name", "")
            row["billing_plan_slug"] = info.get("plan_slug", "")
            row["billing_plan_id"] = info.get("plan_id", None)

        return serialized_data
