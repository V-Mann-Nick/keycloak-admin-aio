import pytest
import test_roles
from dependencies_plugin import depends
from utils import ResourceLifeCycleTest, assert_not_raises

from keycloak_admin_aio import (
    ClientScopeRepresentation,
    KeycloakAdmin,
    RoleRepresentation,
)


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


class WithClientScopeId:
    DEPENDENCIES = [
        TestByIdLifeCycle.dependency_name("create"),
        TestByIdLifeCycle.dependency_name("delete"),
    ]

    @pytest.fixture(scope="class")
    async def client_scope_id(self, keycloak_admin: KeycloakAdmin):
        client_scope_id = await keycloak_admin.client_scopes.create(
            ClientScopeRepresentation(
                name="test_client_scope", protocol="openid-connect"
            )
        )
        yield client_scope_id
        await keycloak_admin.client_scopes.by_id(client_scope_id).delete()


class TestScopeMappings(WithClientScopeId):
    @depends(on=WithClientScopeId.DEPENDENCIES)
    @assert_not_raises
    async def test_get(self, keycloak_admin: KeycloakAdmin, client_scope_id: str):
        await keycloak_admin.client_scopes.by_id(client_scope_id).scope_mappings.get()


@depends(on=WithClientScopeId.DEPENDENCIES)
@depends(
    on=[
        test_roles.TestByIdLifeCycle.dependency_name("create", scope="session"),
        test_roles.TestByIdLifeCycle.dependency_name("get", scope="session"),
        test_roles.TestByIdLifeCycle.dependency_name("delete", scope="session"),
    ],
    scope="session",
)
class TestScopeMappingsRealmLifeCycle(ResourceLifeCycleTest, WithClientScopeId):
    @pytest.fixture(scope="class")
    async def role(self, keycloak_admin: KeycloakAdmin):
        role_name = await keycloak_admin.roles.create(
            RoleRepresentation(name="test_role")
        )
        role = await keycloak_admin.roles.by_name(role_name).get()
        yield role
        await keycloak_admin.roles.by_name(role_name).delete()

    @pytest.fixture(scope="class")
    def create(
        self,
        keycloak_admin: KeycloakAdmin,
        client_scope_id: str,
        role: RoleRepresentation,
    ):
        async def create():
            await keycloak_admin.client_scopes.by_id(
                client_scope_id
            ).scope_mappings.realm.create([role])

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin, client_scope_id: str):
        async def get(_):
            await keycloak_admin.client_scopes.by_id(
                client_scope_id
            ).scope_mappings.realm.get()

        return get

    @pytest.fixture(scope="class")
    def update(self):
        return None

    @pytest.fixture(scope="class")
    def delete(
        self,
        keycloak_admin: KeycloakAdmin,
        client_scope_id: str,
        role: RoleRepresentation,
    ):
        async def delete(_):
            await keycloak_admin.client_scopes.by_id(
                client_scope_id
            ).scope_mappings.realm.delete([role])

        return delete
