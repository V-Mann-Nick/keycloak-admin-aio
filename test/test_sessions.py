import asyncio
from datetime import datetime

import httpx
import pytest
import test_roles

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio._lib.utils import cast_non_optional


async def get_all_admin_cli_sessions(keycloak_admin: KeycloakAdmin):
    clients = await keycloak_admin.clients.get(client_id="admin-cli", search=True)
    admin_cli_client = clients.pop()
    return await keycloak_admin.clients.by_id(
        cast_non_optional(admin_cli_client.id)
    ).user_sessions.get()


class TestById:
    """Test keycloak_admin_aio.sessions.by_id"""

    @pytest.mark.dependency(
        depends=[
            test_roles.TestByNameLifeCycle.dependency_name("get", scope="session"),
            "test/test_clients.py::test_get",
            "test/test_clients.py::test_get_user_sessions",
        ],
        scope="session",
    )
    async def test_delete(self, keycloak_admin: KeycloakAdmin):
        """Test keycloak_admin_aio.sessions.by_id.delete

        Session delete is tested by deleting the session of keycloak_admin_aio itself.
        """
        sessions = await get_all_admin_cli_sessions(keycloak_admin)
        assert len(sessions) > 0
        sessions.sort(key=lambda s: cast_non_optional(s.lastAccess))

        async def delete_session(session_id: str):
            try:
                await keycloak_admin.sessions.by_id(
                    cast_non_optional(session_id)
                ).delete()
            except httpx.HTTPStatusError as ex:
                if ex.response.status_code == httpx.codes.UNAUTHORIZED:
                    # Just terminated its own session
                    return
                raise ex

        await asyncio.gather(
            *[delete_session(cast_non_optional(session.id)) for session in sessions]
        )
        keycloak_admin.access_token_expire = datetime.now()
        try:
            # Try doing anything
            await keycloak_admin.roles.by_name("create-realm").get()
        except httpx.HTTPStatusError as ex:
            if ex.response.status_code == httpx.codes.UNAUTHORIZED:
                pytest.fail(f"Session removal not handled correctly: {ex}")
