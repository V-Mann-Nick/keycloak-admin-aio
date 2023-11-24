import asyncio

import pytest
import test_roles
from test_sessions import get_all_admin_cli_sessions

from keycloak_admin_aio import KeycloakAdmin


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=[
        test_roles.TestByNameLifeCycle.dependency_name("get", scope="session"),
        "test/test_clients.py::test_get",
        "test/test_clients.py::test_get_user_sessions",
    ],
    scope="session",
)
async def test_only_one_session(keycloak_admin: KeycloakAdmin):
    """Make sure that only one session is created when using KeycloakAdmin"""
    sessions = await get_all_admin_cli_sessions(keycloak_admin)
    sessions_count_before = len(sessions)
    async with KeycloakAdmin.with_password(
        server_url="http://localhost:8080", username="testing", password="testing"
    ) as kc:
        await asyncio.gather(
            kc.roles.by_name("create-realm").get(),
            kc.roles.by_name("admin").get(),
        )
    sessions = await get_all_admin_cli_sessions(keycloak_admin)
    sessions_count_after = len(sessions)

    if sessions_count_before + 1 != sessions_count_after:
        pytest.fail("KeycloakAdmin created instantiated to many sessions.")
