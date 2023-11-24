import pytest
import pytest_asyncio
import test_client_scopes
from conftest import KEYCLOAK_ADMIN
from utils import ResourceLifeCycleTest, assert_not_raises

from keycloak_admin_aio import ClientRepresentation, KeycloakAdmin
from keycloak_admin_aio._lib.utils import cast_non_optional
from keycloak_admin_aio.types.types import ClientScopeRepresentation


@pytest.mark.asyncio
@pytest.mark.dependency()
@assert_not_raises
async def test_get(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.clients.get"""
    await keycloak_admin.clients.get()


class TestByIdLifeCycle(ResourceLifeCycleTest):
    """Test keycloak_admin.clients.by_id."""

    @pytest.fixture(scope="class")
    def create(self, keycloak_admin: KeycloakAdmin):
        async def create():
            return await keycloak_admin.clients.create(
                ClientRepresentation(name="test_client")
            )

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin):
        async def get(client_uuid):
            await keycloak_admin.clients.by_id(client_uuid).get()

        return get

    @pytest.fixture(scope="class")
    def update(self, keycloak_admin: KeycloakAdmin):
        async def update(client_uuid):
            await keycloak_admin.clients.by_id(client_uuid).update(
                ClientRepresentation(name="new_name")
            )

        return update

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin):
        async def delete(client_uuid):
            await keycloak_admin.clients.by_id(client_uuid).delete()

        return delete


class TestByIdDefaultClientScopesByIdLifecycle(ResourceLifeCycleTest):
    """Test keycloak_admin.clients.by_id.default_client_scopes."""

    EXTRA_DEPENDENCIES = [
        test_client_scopes.TestByIdLifeCycle.dependency_name(
            "create", scope="session", as_dep=True
        ),
    ]

    @pytest_asyncio.fixture(scope="class")
    async def a_default_client(self, keycloak_admin: KeycloakAdmin):
        clients = await keycloak_admin.clients.get()
        return clients[0]

    @pytest.fixture(scope="class")
    def a_default_client_uuid(self, a_default_client: ClientRepresentation):
        return cast_non_optional(a_default_client.id)

    @pytest_asyncio.fixture(scope="class")
    async def client_scope_id(self, keycloak_admin: KeycloakAdmin):
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

    @pytest.fixture(scope="class")
    def create(
        self,
        keycloak_admin: KeycloakAdmin,
        a_default_client_uuid: str,
        client_scope_id: str,
    ):
        async def create():
            await keycloak_admin.clients.by_id(
                a_default_client_uuid
            ).default_client_scopes.by_id(client_scope_id).create()

        return create

    @pytest.fixture(scope="class")
    def get(
        self,
        keycloak_admin: KeycloakAdmin,
        a_default_client_uuid: str,
    ):
        async def get(_):
            await keycloak_admin.clients.by_id(
                a_default_client_uuid
            ).default_client_scopes.get()

        return get

    @pytest.fixture(scope="class")
    def update(self):
        return None

    @pytest.fixture(scope="class")
    def delete(
        self,
        keycloak_admin: KeycloakAdmin,
        a_default_client_uuid: str,
        client_scope_id: str,
    ):
        async def delete(_):
            await keycloak_admin.clients.by_id(
                a_default_client_uuid
            ).default_client_scopes.by_id(client_scope_id).delete()

        return delete


# == keycloak_admin.clients.by_id.user_sessions ==


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_get"])
async def test_get_user_sessions(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.clients.by_id.user_sessions.get

    We check if the admin user of our current keycloak_admin instance is in
    the list of active user sessions of the admin-cli client we're using for
    testing
    """
    clients = await keycloak_admin.clients.get(client_id="admin-cli", search=True)
    admin_client = clients[0]
    admin_client_uuid = cast_non_optional(admin_client.id)
    user_sessions = await keycloak_admin.clients.by_id(
        admin_client_uuid
    ).user_sessions.get()
    assert KEYCLOAK_ADMIN in [user_session.username for user_session in user_sessions]
