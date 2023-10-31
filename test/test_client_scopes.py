import httpx
import pytest
import pytest_asyncio

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio.types.types import ClientScopeRepresentation


@pytest.fixture(scope="module")
def client_scope_representation():
    return ClientScopeRepresentation(name="test_client_scope")


@pytest_asyncio.fixture(scope="module")
async def client_scope(
    keycloak_admin: KeycloakAdmin,
    client_scope_representation: ClientScopeRepresentation,
):
    client_scope_id = await keycloak_admin.client_scopes.create(
        client_scope_representation
    )
    client_scope = await keycloak_admin.client_scopes.by_id(client_scope_id).get()
    return client_scope


@pytest.fixture(scope="module")
def client_scope_id(client_scope: ClientScopeRepresentation):
    return client_scope.id


@pytest.mark.dependency()
def test_create(client_scope: ClientScopeRepresentation):
    assert client_scope


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create"])
async def test_get_by_id(
    keycloak_admin: KeycloakAdmin,
    client_scope_id: str,
):
    assert await keycloak_admin.client_scopes.by_id(client_scope_id).get()


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create", "test_get_by_id"])
async def test_update_by_id(
    keycloak_admin: KeycloakAdmin,
    client_scope_id: str,
    client_scope: ClientScopeRepresentation,
):
    new_client_scope = ClientScopeRepresentation.from_dict(client_scope.to_dict())
    new_client_scope.name = "new_name"
    await keycloak_admin.client_scopes.by_id(client_scope_id).update(new_client_scope)
    client_scope = await keycloak_admin.client_scopes.by_id(client_scope_id).get()
    assert client_scope.name == "new_name"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create", "test_get_by_id", "test_update_by_id"])
async def test_delete_by_id(keycloak_admin: KeycloakAdmin, client_scope_id: str):
    await keycloak_admin.client_scopes.by_id(client_scope_id).delete()
    with pytest.raises(httpx.HTTPStatusError, match="404 Not Found"):
        await keycloak_admin.client_scopes.by_id(client_scope_id).get()


# TODO: Missing scope_mappings
