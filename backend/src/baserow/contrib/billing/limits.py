"""
Billing plan limit enforcement.

Row limits use live counts from user tables (not TableUsage), because usage
row_count is updated asynchronously via Celery and is often stale or NULL.
"""

import logging

from baserow.contrib.billing.exceptions import PlanLimitExceededError

logger = logging.getLogger(__name__)


def _get_workspace_plan_first_admin(workspace):
    """
    Plan from the first workspace admin (by WorkspaceUser pk) with a usable
    subscription. Used as fallback when the acting user has no membership.
    """

    from baserow.core.models import (
        WORKSPACE_USER_PERMISSION_ADMIN,
        WorkspaceUser,
    )

    admin_users = (
        WorkspaceUser.objects.filter(
            workspace=workspace,
            permissions=WORKSPACE_USER_PERMISSION_ADMIN,
        )
        .select_related("user__subscription__plan")
        .order_by("pk")
    )

    for wu in admin_users:
        sub = getattr(wu.user, "subscription", None)
        if sub and sub.is_usable:
            return sub.plan
    return None


def _resolve_plan_for_row_limit(workspace, acting_user):
    """
    Prefer the subscription of the user creating rows (if they belong to the
    workspace). Otherwise fall back to the first admin's plan.
    """

    from baserow.contrib.billing.handler import BillingHandler
    from baserow.core.models import WorkspaceUser

    if acting_user and getattr(acting_user, "pk", None):
        if WorkspaceUser.objects.filter(
            workspace=workspace, user=acting_user
        ).exists():
            sub = BillingHandler.get_subscription_safe(acting_user)
            if sub and sub.is_usable:
                return sub.plan
    return _get_workspace_plan_first_admin(workspace)


def get_workspace_row_count(workspace):
    """
    Total non-trashed rows across all non-trashed tables in the workspace.
    Uses each table's generated model default manager (excludes trashed rows).
    """

    from baserow.contrib.database.table.models import Table

    qs = Table.objects.filter(
        database__workspace=workspace,
        database__trashed=False,
        trashed=False,
    )
    total = 0
    for table in qs.iterator(chunk_size=32):
        try:
            model = table.get_model()
            total += model.objects.count()
        except Exception:
            logger.exception(
                "Billing row limit: could not count rows for table id=%s", table.id
            )
    return total


def check_row_limit(workspace, acting_user=None, rows_to_add=1):
    """
    Raise PlanLimitExceededError if adding rows would exceed the effective plan limit.
    """

    plan = _resolve_plan_for_row_limit(workspace, acting_user)
    if plan is None:
        return

    max_rows = plan.max_rows_per_workspace
    if max_rows is None:
        return

    current = get_workspace_row_count(workspace)
    if current + rows_to_add > max_rows:
        raise PlanLimitExceededError(
            limit_type="max_rows_per_workspace",
            current=current,
            maximum=max_rows,
        )


def check_row_limit_for_table(table, acting_user=None, rows_to_add=1):
    """
    Resolve workspace from table and enforce row limit.
    """

    try:
        workspace = table.database.workspace
    except Exception:
        return
    if workspace is None:
        return
    check_row_limit(workspace, acting_user=acting_user, rows_to_add=rows_to_add)


def check_workspace_limit(user):
    """
    Raise PlanLimitExceededError if the user already owns as many workspaces
    as their plan allows.
    """

    from baserow.contrib.billing.handler import BillingHandler
    from baserow.core.models import (
        WORKSPACE_USER_PERMISSION_ADMIN,
        WorkspaceUser,
    )

    sub = BillingHandler.get_subscription_safe(user)
    if sub is None or not sub.is_usable:
        return

    max_ws = sub.plan.max_workspaces
    if max_ws is None:
        return

    current = WorkspaceUser.objects.filter(
        user=user,
        permissions=WORKSPACE_USER_PERMISSION_ADMIN,
    ).count()

    if current >= max_ws:
        raise PlanLimitExceededError(
            limit_type="max_workspaces",
            current=current,
            maximum=max_ws,
        )
