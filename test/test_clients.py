import httpx
import pytest
import pytest_asyncio
from conftest import KEYCLOAK_ADMIN

from keycloak_admin_aio import ClientRepresentation, KeycloakAdmin
from keycloak_admin_aio._lib.utils import cast_non_optional
from keycloak_admin_aio.types.types import ClientScopeRepresentation

# == keycloak_admin.clients ==


@pytest_asyncio.fixture(scope="module")
async def client_uuid(keycloak_admin: KeycloakAdmin):
    client_uuid = await keycloak_admin.clients.create(
        ClientRepresentation(name="test_client")
    )
    return client_uuid


@pytest.mark.dependency()
def test_create(client_uuid: str):
    """Create a client by using the fixture"""
    assert client_uuid


@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_get(keycloak_admin: KeycloakAdmin):
    clients = await keycloak_admin.clients.get()
    assert len(clients) > 0


# == keycloak_admin.clients.by_id ==


@pytest_asyncio.fixture(scope="module")
async def client(keycloak_admin: KeycloakAdmin, client_uuid: str):
    client = await keycloak_admin.clients.by_id(client_uuid).get()
    return client


@pytest.mark.dependency(depends=["test_create"])
def test_get_by_id(
    client: ClientRepresentation,
):
    """Try getting the previously created client by id by using the fixture"""
    assert client


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create", "test_get_by_id"])
async def test_update_by_id(
    keycloak_admin: KeycloakAdmin, client_uuid: str, client: ClientRepresentation
):
    """Try updating the previously created client by id"""
    new_client = ClientRepresentation.from_dict(client.to_dict())
    new_client.name = "new_name"
    await keycloak_admin.clients.by_id(client_uuid).update(new_client)
    client = await keycloak_admin.clients.by_id(client_uuid).get()
    assert client.name == "new_name"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create", "test_get_by_id", "test_update_by_id"])
async def test_delete_by_id(keycloak_admin: KeycloakAdmin, client_uuid: str):
    """Try deleting the previously created client by id"""
    await keycloak_admin.clients.by_id(client_uuid).delete()
    with pytest.raises(httpx.HTTPStatusError, match="404 Not Found"):
        await keycloak_admin.clients.by_id(client_uuid).get()


# == keycloak_admin.clients.by_id.default_client_scopes ==


@pytest_asyncio.fixture(scope="module")
async def a_default_client(keycloak_admin: KeycloakAdmin):
    clients = await keycloak_admin.clients.get()
    return clients[0]


@pytest.fixture(scope="module")
def a_default_client_uuid(a_default_client: ClientRepresentation):
    return cast_non_optional(a_default_client.id)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_get"])
async def test_get_default_client_scopes(
    keycloak_admin: KeycloakAdmin, a_default_client_uuid: str
):
    """Try getting the default client scopes for a client"""
    client_scopes = await keycloak_admin.clients.by_id(
        a_default_client_uuid
    ).default_client_scopes.get()
    assert len(client_scopes) > 0


# == keycloak_admin.clients.by_id.default_client_scopes.by_id ==


@pytest_asyncio.fixture(scope="module")
async def client_scope_id(keycloak_admin: KeycloakAdmin):
    client_scope_id = await keycloak_admin.client_scopes.create(
        ClientScopeRepresentation(
            name="test_client_scope",
            # Although Keycloak accepts create without protocol, the resulting
            # resource is buggy and cannot be added to a client
            protocol="openid-connect",
        )
    )
    yield client_scope_id
    await keycloak_admin.client_scopes.by_id(client_scope_id).delete()


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=[
        "test/test_clients.py::test_get_default_client_scopes",
        "test/test_client_scopes.py::test_create",
        "test/test_client_scopes.py::test_get_by_id",
        "test/test_client_scopes.py::test_delete_by_id",
    ],
    scope="session",
)
async def test_add_default_client_scope(
    keycloak_admin: KeycloakAdmin,
    a_default_client_uuid: str,
    client_scope_id: str,
):
    """Try adding a client scope to the default client scopes"""
    await keycloak_admin.clients.by_id(
        a_default_client_uuid
    ).default_client_scopes.by_id(client_scope_id).create()
    client_scopes = await keycloak_admin.clients.by_id(
        a_default_client_uuid
    ).default_client_scopes.get()
    assert client_scope_id in [client_scope.id for client_scope in client_scopes]


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=[
        "test/test_clients.py::test_get_default_client_scopes",
        "test/test_clients.py::test_add_default_client_scope",
        "test/test_client_scopes.py::test_create",
        "test/test_client_scopes.py::test_get_by_id",
        "test/test_client_scopes.py::test_delete_by_id",
    ],
    scope="session",
)
async def test_remove_default_client_scope(
    keycloak_admin: KeycloakAdmin,
    a_default_client_uuid: str,
    client_scope_id: str,
):
    """Try deleting the previously added default client scope"""
    await keycloak_admin.clients.by_id(
        a_default_client_uuid
    ).default_client_scopes.by_id(client_scope_id).delete()
    client_scopes = await keycloak_admin.clients.by_id(
        a_default_client_uuid
    ).default_client_scopes.get()
    assert client_scope_id not in [client_scope.id for client_scope in client_scopes]


# == keycloak_admin.clients.by_id.user_sessions ==


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_get"])
async def test_get_user_sessions(keycloak_admin: KeycloakAdmin):
    """We check if the admin user of our current keycloak_admin instance is in
    the list of active user sessions of the admin-cli client we're using for
    testing"""
    clients = await keycloak_admin.clients.get(client_id="admin-cli", search=True)
    admin_client = clients[0]
    admin_client_uuid = cast_non_optional(admin_client.id)
    user_sessions = await keycloak_admin.clients.by_id(
        admin_client_uuid
    ).user_sessions.get()
    assert KEYCLOAK_ADMIN in [user_session.username for user_session in user_sessions]
