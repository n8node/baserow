from django.test import override_settings

import pytest
from baserow_enterprise_tests.role.test_role_permission_manager import (
    _populate_test_data,
)

from baserow.core.models import WorkspaceUser
from baserow_enterprise.role.handler import RoleAssignmentHandler
from baserow_enterprise.role.member_data_types import EnterpriseRolesDataType


@pytest.fixture(autouse=True)
def enable_enterprise_for_all_tests_here(enable_enterprise):
    pass


@pytest.mark.django_db
@override_settings(
    PERMISSION_MANAGERS=["core", "staff", "member", "basic", "role"],
)
def test_roles_member_data_type(data_fixture, enterprise_data_fixture, synced_roles):
    (
        admin,
        builder,
        editor,
        viewer,
        viewer_plus,
        builder_less,
        no_access,
        workspace_1,
        workspace_2,
        database_1,
        database_2,
        database_3,
        table_1_1,
        table_1_2,
        table_2_1,
        table_2_2,
    ) = _populate_test_data(data_fixture, enterprise_data_fixture)

    users = [admin, builder, editor, viewer, viewer_plus, builder_less, no_access]

    result = EnterpriseRolesDataType().annotate_serialized_workspace_members_data(
        workspace_1,
        [
            {
                "user_id": u.id,
                "permissions": RoleAssignmentHandler()
                .get_current_role_assignment(u, workspace_1)
                .role.uid,
            }
            for u in users
        ],
        admin,
    )
    assert result == [
        {
            "permissions": "ADMIN",
            "role_uid": "ADMIN",
            "user_id": admin.id,
            "highest_role_uid": "ADMIN",
        },
        {
            "permissions": "BUILDER",
            "role_uid": "BUILDER",
            "user_id": builder.id,
            "highest_role_uid": "BUILDER",
        },
        {
            "permissions": "EDITOR",
            "role_uid": "EDITOR",
            "user_id": editor.id,
            "highest_role_uid": "EDITOR",
        },
        {
            "permissions": "VIEWER",
            "role_uid": "VIEWER",
            "user_id": viewer.id,
            "highest_role_uid": "VIEWER",
        },
        {
            "permissions": "VIEWER",
            "role_uid": "VIEWER",
            "user_id": viewer_plus.id,
            "highest_role_uid": "BUILDER",
        },
        {
            "permissions": "BUILDER",
            "role_uid": "BUILDER",
            "user_id": builder_less.id,
            "highest_role_uid": "BUILDER",
        },
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": no_access.id,
            "highest_role_uid": "NO_ACCESS",
        },
    ]

    result = EnterpriseRolesDataType().annotate_serialized_workspace_members_data(
        workspace_2,
        [
            {
                "user_id": u.id,
                "permissions": RoleAssignmentHandler()
                .get_current_role_assignment(u, workspace_2)
                .role.uid,
            }
            for u in users
        ],
        WorkspaceUser.objects.get(permissions="ADMIN", workspace=workspace_2).user,
    )
    assert result == [
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": admin.id,
            "highest_role_uid": "NO_ACCESS",
        },
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": builder.id,
            "highest_role_uid": "BUILDER",
        },
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": editor.id,
            "highest_role_uid": "NO_ACCESS",
        },
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": viewer.id,
            "highest_role_uid": "NO_ACCESS",
        },
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": viewer_plus.id,
            "highest_role_uid": "NO_ACCESS",
        },
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": builder_less.id,
            "highest_role_uid": "NO_ACCESS",
        },
        {
            "permissions": "NO_ACCESS",
            "role_uid": "NO_ACCESS",
            "user_id": no_access.id,
            "highest_role_uid": "NO_ACCESS",
        },
    ]


@pytest.mark.django_db
@override_settings(
    PERMISSION_MANAGERS=["core", "staff", "member", "basic", "role"],
)
def test_roles_member_data_type_doesnt_expose_to_users_without_read_role(
    data_fixture, enterprise_data_fixture, synced_roles
):
    (
        admin,
        builder,
        editor,
        viewer,
        viewer_plus,
        builder_less,
        no_access,
        workspace_1,
        workspace_2,
        database_1,
        database_2,
        database_3,
        table_1_1,
        table_1_2,
        table_2_1,
        table_2_2,
    ) = _populate_test_data(data_fixture, enterprise_data_fixture)

    users = [admin, builder, editor, viewer, viewer_plus, builder_less, no_access]

    serialized_users_pre_annotation = [
        {
            "user_id": u.id,
            "permissions": RoleAssignmentHandler()
            .get_current_role_assignment(u, workspace_1)
            .role.uid,
        }
        for u in users
    ]
    result = EnterpriseRolesDataType().annotate_serialized_workspace_members_data(
        workspace_1,
        list(serialized_users_pre_annotation),
        viewer,
    )
    assert result == serialized_users_pre_annotation


@pytest.mark.django_db
@override_settings(
    PERMISSION_MANAGERS=["core", "staff", "member", "basic", "role"],
)
def test_roles_member_data_type_without_seat_usage_summary(
    data_fixture, enterprise_data_fixture, synced_roles, mocker
):
    user = data_fixture.create_user()
    workspace = enterprise_data_fixture.create_workspace(user=user)

    license_plugin = mocker.Mock()
    license_plugin.get_seat_usage_for_workspace.return_value = None
    mocker.patch(
        "baserow_enterprise.role.member_data_types.plugin_registry.get_by_type",
        return_value=mocker.Mock(get_license_plugin=mocker.Mock(return_value=license_plugin)),
    )

    serialized_data = [{"user_id": user.id, "permissions": "ADMIN"}]

    result = EnterpriseRolesDataType().annotate_serialized_workspace_members_data(
        workspace, serialized_data, user
    )

    assert result == [
        {
            "user_id": user.id,
            "permissions": "ADMIN",
            "role_uid": "ADMIN",
            "highest_role_uid": None,
        }
    ]
