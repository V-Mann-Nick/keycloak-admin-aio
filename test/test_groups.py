import pytest
from utils import ResourceLifeCycleTest

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio.types.types import GroupRepresentation


@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_get(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.groups.get"""
    await keycloak_admin.groups.get()


@pytest.mark.asyncio
async def test_count(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.groups.count"""
    await keycloak_admin.groups.count()


class TestGroupByIdLifeCycle(ResourceLifeCycleTest):
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


# TODO: more tests missing
