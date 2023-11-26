import pytest
import test_groups
import test_roles
from dependencies_plugin import depends
from utils import ResourceLifeCycleTest, assert_not_raises

from keycloak_admin_aio import (
    GroupRepresentation,
    KeycloakAdmin,
    RoleRepresentation,
    UserRepresentation,
)


@assert_not_raises
async def test_get(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.users.get"""
    await keycloak_admin.users.get()


@assert_not_raises
async def test_count(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.users.count"""
    await keycloak_admin.users.count()


class TestByIdLifeCycle(ResourceLifeCycleTest):
    """Test keycloak_admin.users & keycloak_admin.users.by_id"""

    @pytest.fixture(scope="class")
    def create(self, keycloak_admin: KeycloakAdmin):
        async def create():
            return await keycloak_admin.users.create(
                UserRepresentation(username="test_user")
            )

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin):
        async def get(user_id: str):
            return await keycloak_admin.users.by_id(user_id).get()

        return get

    @pytest.fixture(scope="class")
    def update(self, keycloak_admin: KeycloakAdmin):
        async def update(user_id: str):
            await keycloak_admin.users.by_id(user_id).update(
                UserRepresentation(username="test_user", email="test@test.com")
            )

        return update

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin):
        async def delete(user_id: str):
            await keycloak_admin.users.by_id(user_id).delete()

        return delete


class WithUserIdFixture:
    DEPENDENCIES = [
        TestByIdLifeCycle.dependency_name("create"),
        TestByIdLifeCycle.dependency_name("delete"),
    ]

    @pytest.fixture(scope="class")
    async def user_id(self, keycloak_admin: KeycloakAdmin):
        user_id = await keycloak_admin.users.create(
            UserRepresentation(username="test_user")
        )
        yield user_id
        await keycloak_admin.users.by_id(user_id).delete()


@depends(
    on=[
        test_groups.TestByIdLifeCycle.dependency_name("create", scope="session"),
        test_groups.TestByIdLifeCycle.dependency_name("delete", scope="session"),
    ],
    scope="session",
)
@depends(on=WithUserIdFixture.DEPENDENCIES)
class TestByIdGroupsByIdLifeCycle(ResourceLifeCycleTest, WithUserIdFixture):
    """Test keycloak_admin.users.by_id.groups & keycloak_admin.users.by_id.groups.by_id"""

    @pytest.fixture(scope="class")
    async def group_id(self, keycloak_admin: KeycloakAdmin):
        group_id = await keycloak_admin.groups.create(
            GroupRepresentation(name="test_group")
        )
        yield group_id
        await keycloak_admin.groups.by_id(group_id).delete()

    @pytest.fixture(scope="class")
    def create(self, keycloak_admin: KeycloakAdmin, group_id: str, user_id: str):
        async def create():
            await keycloak_admin.users.by_id(user_id).groups.by_id(group_id).create()

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin, user_id: str):
        async def get(_):
            await keycloak_admin.users.by_id(user_id).groups.get()

        return get

    # FIXME: dependency
    @assert_not_raises
    async def test_count(self, keycloak_admin: KeycloakAdmin, user_id: str):
        await keycloak_admin.users.by_id(user_id).groups.count()

    @pytest.fixture(scope="class")
    def update(self):
        return None

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin, group_id: str, user_id: str):
        async def delete(_):
            await keycloak_admin.users.by_id(user_id).groups.by_id(group_id).delete()

        return delete


class TestRoleMappings(WithUserIdFixture):
    @depends(on=WithUserIdFixture.DEPENDENCIES)
    @assert_not_raises
    async def test_get(self, keycloak_admin: KeycloakAdmin, user_id: str):
        """Test keycloak_admin.users.by_id.role_mappings.get"""
        await keycloak_admin.users.by_id(user_id).role_mappings.get()


@depends(
    on=[
        test_roles.TestByNameLifeCycle.dependency_name("create", scope="session"),
        test_roles.TestByNameLifeCycle.dependency_name("get", scope="session"),
        test_roles.TestByNameLifeCycle.dependency_name("delete", scope="session"),
    ],
    scope="session",
)
@depends(on=WithUserIdFixture.DEPENDENCIES)
class TestRoleMappingsRealmLifeCycle(ResourceLifeCycleTest, WithUserIdFixture):
    """Test keycloak_admin.users.by_id.role_mappings.realm"""

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
        self, keycloak_admin: KeycloakAdmin, user_id: str, role: RoleRepresentation
    ):
        async def create():
            await keycloak_admin.users.by_id(user_id).role_mappings.realm.create([role])

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin, user_id: str):
        async def get(_):
            await keycloak_admin.users.by_id(user_id).role_mappings.realm.get()

        return get

    @pytest.fixture(scope="class")
    def update(self):
        return None

    @pytest.fixture(scope="class")
    def delete(
        self, keycloak_admin: KeycloakAdmin, user_id: str, role: RoleRepresentation
    ):
        async def delete(_):
            await keycloak_admin.users.by_id(user_id).role_mappings.realm.delete([role])

        return delete

    @assert_not_raises
    async def test_available(self, keycloak_admin: KeycloakAdmin, user_id: str):
        """Test keycloak_admin.users.by_id.role_mappings.realm.available"""
        await keycloak_admin.users.by_id(user_id).role_mappings.realm.available()

    @assert_not_raises
    async def test_composite(self, keycloak_admin: KeycloakAdmin, user_id: str):
        """Test keycloak_admin.users.by_id.role_mappings.realm.composite"""
        await keycloak_admin.users.by_id(user_id).role_mappings.realm.composite()
