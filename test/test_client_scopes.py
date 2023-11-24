import pytest
from utils import ResourceLifeCycleTest, assert_not_raises

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio.types.types import ClientScopeRepresentation


@pytest.mark.asyncio
@pytest.mark.dependency()
@assert_not_raises
async def test_get(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.client_scopes.get"""
    await keycloak_admin.client_scopes.get()


class TestByIdLifeCycle(ResourceLifeCycleTest):
    """Test keycloak_admin.client_scopes.by_id."""

    @pytest.fixture(scope="class")
    def create(self, keycloak_admin: KeycloakAdmin):
        async def create():
            return await keycloak_admin.client_scopes.create(
                ClientScopeRepresentation(
                    name="test_client_scope", protocol="openid-connect"
                )
            )

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin):
        async def get(client_scope_id):
            await keycloak_admin.client_scopes.by_id(client_scope_id).get()

        return get

    @pytest.fixture(scope="class")
    def update(self, keycloak_admin: KeycloakAdmin):
        async def update(client_scope_id):
            await keycloak_admin.client_scopes.by_id(client_scope_id).update(
                ClientScopeRepresentation(name="new_name")
            )

        return update

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin):
        async def delete(client_scope_id):
            await keycloak_admin.client_scopes.by_id(client_scope_id).delete()

        return delete


# TODO: Missing scope_mappings
