"""
Billing plan limit enforcement.

Provides helpers that check whether a workspace (via its owner's subscription)
is within the allowed plan limits, and signal receivers that block operations
when limits are exceeded.
"""

import logging

from django.db.models import Sum
from django.db.models.functions import Coalesce

from baserow.contrib.billing.exceptions import PlanLimitExceededError

logger = logging.getLogger(__name__)


def _get_workspace_plan(workspace):
    """
    Return the Plan for the workspace owner (first admin by pk).
    Returns None if no admin has an active subscription.
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


def get_workspace_row_count(workspace):
    """
    Fast row count for all non-trashed tables in the workspace using the
    cached TableUsage.row_count (updated by the periodic celery task).
    """

    from baserow.contrib.database.table.models import Table

    result = (
        Table.objects.filter(
            database__workspace=workspace,
            database__trashed=False,
            trashed=False,
        )
        .aggregate(total=Coalesce(Sum("usage__row_count"), 0))
    )
    return result["total"]


def check_row_limit(workspace, rows_to_add=1):
    """
    Raise PlanLimitExceededError if adding `rows_to_add` rows would exceed
    the workspace owner's plan limit.
    """

    plan = _get_workspace_plan(workspace)
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


def check_row_limit_for_table(table, rows_to_add=1):
    """
    Convenience wrapper: resolves workspace from a Table instance
    and delegates to check_row_limit.
    """

    try:
        workspace = table.database.workspace
    except Exception:
        return
    if workspace is None:
        return
    check_row_limit(workspace, rows_to_add=rows_to_add)


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


# ── Signal receivers ──────────────────────────────────────────────────


def on_before_rows_create(sender, **kwargs):
    """
    Connected to `before_rows_create` signal.
    Blocks row creation if workspace row limit would be exceeded.
    The signal doesn't carry the number of rows, so we check ≥ limit
    (i.e. at least 1 row would exceed).
    """

    table = kwargs.get("table")
    if table is None:
        return

    try:
        check_row_limit_for_table(table, rows_to_add=1)
    except PlanLimitExceededError:
        raise
    except Exception:
        logger.exception("Error checking row limit")
