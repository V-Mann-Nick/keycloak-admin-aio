import pytest
from utils import ResourceLifeCycleTest, assert_not_raises

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio.types.types import GroupRepresentation


@pytest.mark.dependency()
@assert_not_raises
async def test_get(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.groups.get"""
    await keycloak_admin.groups.get()


@pytest.mark.dependency()
@assert_not_raises
async def test_count(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.groups.count"""
    await keycloak_admin.groups.count()


class TestByIdLifeCycle(ResourceLifeCycleTest):
    """Test keycloak_admin.groups & keycloak_admin.groups.by_id"""

    @pytest.fixture(scope="class")
    def create(self, keycloak_admin: KeycloakAdmin):
        async def create():
            return await keycloak_admin.groups.create(
                GroupRepresentation(name="test_group")
            )

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin):
        async def get(group_id: str):
            await keycloak_admin.groups.by_id(group_id).get()

        return get

    @pytest.fixture(scope="class")
    def update(self, keycloak_admin: KeycloakAdmin):
        async def update(group_id: str):
            await keycloak_admin.groups.by_id(group_id).update(
                GroupRepresentation(name="test_group_updated")
            )

        return update

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin):
        async def delete(group_id: str):
            await keycloak_admin.groups.by_id(group_id).delete()

        return delete


class WithGroupIdFixture:
    DEPENDENCIES = [
        TestByIdLifeCycle.dependency_name("create"),
        TestByIdLifeCycle.dependency_name("delete"),
    ]

    @pytest.fixture(scope="class")
    async def group_id(self, keycloak_admin: KeycloakAdmin):
        group_id = await keycloak_admin.groups.create(
            GroupRepresentation(name="test_group")
        )
        yield group_id
        await keycloak_admin.groups.by_id(group_id).delete()


class TestMembers(WithGroupIdFixture):
    """Test keycloak_admin.groups.by_id.members"""

    @pytest.mark.dependency(depends=WithGroupIdFixture.DEPENDENCIES)
    @assert_not_raises
    async def test_get(self, keycloak_admin: KeycloakAdmin, group_id: str):
        """Test keycloak_admin.groups.by_id.members.get"""
        await keycloak_admin.groups.by_id(group_id).members.get()


class TestChildren(WithGroupIdFixture):
    """Test keycloak_admin.groups.by_id.children"""

    @pytest.fixture(scope="class")
    async def other_group(self, keycloak_admin: KeycloakAdmin):
        group_id = await keycloak_admin.groups.create(
            GroupRepresentation(name="test_group_2")
        )
        group = await keycloak_admin.groups.by_id(group_id).get()
        yield group
        await keycloak_admin.groups.by_id(group_id).delete()

    @pytest.mark.dependency(
        depends=[
            *WithGroupIdFixture.DEPENDENCIES,
            TestByIdLifeCycle.dependency_name("create"),
            TestByIdLifeCycle.dependency_name("get"),
            TestByIdLifeCycle.dependency_name("delete"),
        ]
    )
    @assert_not_raises
    async def test_create(
        self,
        keycloak_admin: KeycloakAdmin,
        group_id: str,
        other_group: GroupRepresentation,
    ):
        await keycloak_admin.groups.by_id(group_id).children.create(other_group)
