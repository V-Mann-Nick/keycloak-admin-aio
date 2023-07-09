import asyncio
from datetime import datetime

import httpx
import pytest
from fixtures import event_loop, keycloak_admin

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio._lib.utils import cast_non_optional


async def get_all_admin_cli_sessions(keycloak_admin: KeycloakAdmin):
    clients = await keycloak_admin.clients.get(client_id="admin-cli", search=True)
    admin_cli_client = clients.pop()
    return await keycloak_admin.clients.by_id(
        cast_non_optional(admin_cli_client.id)
    ).user_sessions.get()


@pytest.mark.asyncio
async def test_session_remove_handle(keycloak_admin: KeycloakAdmin):
    sessions = await get_all_admin_cli_sessions(keycloak_admin)
    assert len(sessions) > 0
    sessions.sort(key=lambda s: cast_non_optional(s.lastAccess))

    async def delete_session(session_id: str):
        try:
            await keycloak_admin.sessions.by_id(cast_non_optional(session_id)).delete()
        except httpx.HTTPStatusError as ex:
            if ex.response.status_code != httpx.codes.UNAUTHORIZED:
                raise ex
            # Just terminated its own session

    await asyncio.gather(
        *[delete_session(cast_non_optional(session.id)) for session in sessions]
    )
    keycloak_admin.access_token_expire = datetime.now()
    try:
        # Try doing anything
        await keycloak_admin.roles.by_name("create-realm").get()
    except httpx.HTTPStatusError as ex:
        if ex.response.status_code == 401:
            pytest.fail(f"Session removal not handled correctly: {ex}")


@pytest.mark.asyncio
async def test_only_one_session(keycloak_admin: KeycloakAdmin):
    sessions = await get_all_admin_cli_sessions(keycloak_admin)
    sessions_count_before = len(sessions)
    async with KeycloakAdmin.with_password(
        server_url="http://localhost:8080", username="testing", password="testing"
    ) as kc:
        await asyncio.gather(
            kc.roles.by_name("create-realm").get(),
            kc.roles.by_name("admin").get(),
            kc.roles.by_name("admin").get(),
        )
    sessions = await get_all_admin_cli_sessions(keycloak_admin)
    sessions_count_after = len(sessions)

    if sessions_count_before + 1 != sessions_count_after:
        pytest.fail("KeycloakAdmin created instantiated to many sessions.")
