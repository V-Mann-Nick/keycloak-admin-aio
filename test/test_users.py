import pytest
import pytest_asyncio
import test_groups
from utils import ResourceLifeCycleTest, assert_not_raises

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio.types.types import GroupRepresentation, UserRepresentation


@pytest.mark.asyncio
@pytest.mark.dependency()
@assert_not_raises("Could not get users")
async def test_get(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.users.get""" ""
    await keycloak_admin.users.get()


@pytest.mark.asyncio
@assert_not_raises("Could not count users")
async def test_count(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.users.count""" ""
    await keycloak_admin.users.count()


class TestUserByIdLifeCycle(ResourceLifeCycleTest):
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


class TestUserByIdGroupsLifeCycle(ResourceLifeCycleTest):
    """Test keycloak_admin.users.by_id.groups & keycloak_admin.users.by_id.groups.by_id"""

    EXTRA_DEPENDENCIES = [
        (
            test_groups.TestGroupByIdLifeCycle.dependency_name(
                "create", scope="session"
            ),
            "session",
        ),
        (
            test_groups.TestGroupByIdLifeCycle.dependency_name(
                "delete", scope="session"
            ),
            "session",
        ),
        TestUserByIdLifeCycle.dependency_name("create"),
        TestUserByIdLifeCycle.dependency_name("delete"),
    ]

    @pytest_asyncio.fixture(scope="class")
    async def group_id(self, keycloak_admin: KeycloakAdmin):
        group_id = await keycloak_admin.groups.create(
            GroupRepresentation(name="test_group")
        )
        yield group_id
        await keycloak_admin.groups.by_id(group_id).delete()

    @pytest_asyncio.fixture(scope="class")
    async def user_id(self, keycloak_admin: KeycloakAdmin, group_id: str):
        user_id = await keycloak_admin.users.create(
            UserRepresentation(username="test_user_2")
        )
        await keycloak_admin.users.by_id(user_id).groups.by_id(group_id).create()
        yield user_id
        await keycloak_admin.users.by_id(user_id).delete()

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

    @pytest.mark.asyncio
    @pytest.mark.order(before="test_delete")
    @pytest.mark.dependency()
    @assert_not_raises("Could not count groups")
    async def test_count(self, keycloak_admin: KeycloakAdmin, user_id: str):
        await keycloak_admin.users.by_id(user_id).groups.count()

    @pytest.fixture(scope="class")
    def update(self):
        return None

    EXTRA_DEPENDENCIES_DELETE = [("test_count", "class")]

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin, group_id: str, user_id: str):
        async def delete(_):
            await keycloak_admin.users.by_id(user_id).groups.by_id(group_id).delete()

        return delete


@pytest_asyncio.fixture(scope="class")
async def user_id(keycloak_admin: KeycloakAdmin):
    user_id = await keycloak_admin.users.create(
        UserRepresentation(username="test_user_3")
    )
    yield user_id
    await keycloak_admin.users.by_id(user_id).delete()


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=[
        TestUserByIdLifeCycle.dependency_name("create"),
        TestUserByIdLifeCycle.dependency_name("delete"),
    ]
)
async def test_role_mappings(keycloak_admin: KeycloakAdmin, user_id: str):
    """Test keycloak_admin.users.by_id.role_mappings.get"""
    try:
        await keycloak_admin.users.by_id(user_id).role_mappings.get()
    except Exception as e:
        assert False, f"Failed to get role mappings: {e}"


# == keycloak_admin.users.by_id.role_mappings.realm ==

# TODO
