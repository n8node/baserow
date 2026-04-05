"""
Billing plan limit enforcement.

Row limits use live counts from user tables (not TableUsage), because usage
row_count is updated asynchronously via Celery and is often stale or NULL.
"""

import logging

from django.db.models import Sum

from baserow.contrib.billing.exceptions import PlanLimitExceededError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Plan resolution helpers
# ---------------------------------------------------------------------------


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


def _resolve_plan_for_workspace(workspace, acting_user=None):
    """
    Prefer the subscription of the acting user (if they belong to the
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


def _resolve_plan_for_user(user):
    """Get the active plan for a specific user (or ``None``)."""

    from baserow.contrib.billing.handler import BillingHandler

    if user is None or not getattr(user, "pk", None):
        return None
    sub = BillingHandler.get_subscription_safe(user)
    if sub and sub.is_usable:
        return sub.plan
    return None


# ---------------------------------------------------------------------------
# Row limits
# ---------------------------------------------------------------------------


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

    plan = _resolve_plan_for_workspace(workspace, acting_user)
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


# ---------------------------------------------------------------------------
# Workspace limits
# ---------------------------------------------------------------------------


def check_workspace_limit(user):
    """
    Raise PlanLimitExceededError if the user already owns as many workspaces
    as their plan allows.
    """

    from baserow.core.models import (
        WORKSPACE_USER_PERMISSION_ADMIN,
        WorkspaceUser,
    )

    plan = _resolve_plan_for_user(user)
    if plan is None:
        return

    max_ws = plan.max_workspaces
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


# ---------------------------------------------------------------------------
# Collaborator limits
# ---------------------------------------------------------------------------


def check_collaborator_limit(workspace, acting_user=None):
    """
    Raise PlanLimitExceededError if the workspace already has the maximum
    number of collaborators allowed by the governing plan.
    """

    from baserow.core.models import WorkspaceUser

    plan = _resolve_plan_for_workspace(workspace, acting_user)
    if plan is None:
        return

    max_collabs = plan.max_collaborators_per_workspace
    if max_collabs is None:
        return

    current = WorkspaceUser.objects.filter(workspace=workspace).count()
    if current >= max_collabs:
        raise PlanLimitExceededError(
            limit_type="max_collaborators_per_workspace",
            current=current,
            maximum=max_collabs,
        )


# ---------------------------------------------------------------------------
# Storage limits
# ---------------------------------------------------------------------------


def check_storage_limit(user, file_size_bytes):
    """
    Raise PlanLimitExceededError if the user's total stored files plus the
    new file would exceed ``max_storage_mb``.

    Total is calculated as ``SUM(UserFile.size)`` for files uploaded by
    this user (not soft-deleted).
    """

    from baserow.core.user_files.models import UserFile

    plan = _resolve_plan_for_user(user)
    if plan is None:
        return

    max_storage = plan.max_storage_mb
    if max_storage is None:
        return

    total_bytes = (
        UserFile.objects.filter(uploaded_by=user, deleted_at__isnull=True).aggregate(
            total=Sum("size")
        )["total"]
        or 0
    )
    new_total_mb = (total_bytes + file_size_bytes) / (1024 * 1024)

    if new_total_mb > max_storage:
        raise PlanLimitExceededError(
            limit_type="max_storage_mb",
            current=int(total_bytes / (1024 * 1024)),
            maximum=max_storage,
        )


# ---------------------------------------------------------------------------
# Per-file size limit
# ---------------------------------------------------------------------------


def check_file_size_limit(user, file_size_bytes):
    """
    Raise PlanLimitExceededError if a single file exceeds the plan's
    ``max_file_upload_size_mb`` limit.
    """

    plan = _resolve_plan_for_user(user)
    if plan is None:
        return

    max_file_mb = plan.max_file_upload_size_mb
    if max_file_mb is None:
        return

    max_file_bytes = max_file_mb * 1024 * 1024
    if file_size_bytes > max_file_bytes:
        raise PlanLimitExceededError(
            limit_type="max_file_upload_size_mb",
            current=int(file_size_bytes / (1024 * 1024)),
            maximum=max_file_mb,
        )
