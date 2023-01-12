import httpx
import pytest

from fixtures import keycloak_admin, event_loop
from keycloak_admin_aio import KeycloakAdmin, UserRepresentation


@pytest.fixture
async def user_id(keycloak_admin: KeycloakAdmin):
    user_id = await keycloak_admin.users.create(
        UserRepresentation(email="test@test.com", username="test")
    )
    yield user_id
    await keycloak_admin.users.by_id(user_id).delete()


@pytest.mark.asyncio
async def test_get_brute_force_status(keycloak_admin: KeycloakAdmin, user_id: str):
    status = await keycloak_admin.attack_detection.brute_force.users.by_id(
        user_id
    ).get()
    assert status is not None
    assert type(status) is dict


@pytest.mark.asyncio
async def test_clear_login_failures(keycloak_admin: KeycloakAdmin):
    try:
        await keycloak_admin.attack_detection.brute_force.users.delete()
    except httpx.HTTPStatusError as ex:
        assert False, ex


@pytest.mark.asyncio
async def test_clear_login_failures_for_user(
    keycloak_admin: KeycloakAdmin, user_id: str
):
    try:
        await keycloak_admin.attack_detection.brute_force.users.by_id(user_id).delete()
    except httpx.HTTPStatusError as ex:
        assert False, ex
