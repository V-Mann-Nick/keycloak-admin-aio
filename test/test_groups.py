import pytest
import pytest_asyncio

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio.types.types import GroupRepresentation

# == keycloak_admin.groups ==


@pytest_asyncio.fixture(scope="module")
async def group_id(keycloak_admin: KeycloakAdmin):
    group_id = await keycloak_admin.groups.create(
        GroupRepresentation(name="test_group")
    )
    return group_id


@pytest.mark.dependency()
def test_create(group_id: str):
    """Create a group by using the fixture"""
    assert group_id


@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_get(keycloak_admin: KeycloakAdmin):
    groups = await keycloak_admin.groups.get()
    assert len(groups) > 0


@pytest.mark.asyncio
async def test_count(keycloak_admin: KeycloakAdmin):
    count = await keycloak_admin.groups.count()
    assert count > 0


# == keycloak_admin.groups.by_id ==


@pytest_asyncio.fixture(scope="module")
async def group(keycloak_admin: KeycloakAdmin, group_id: str):
    group = await keycloak_admin.groups.by_id(group_id).get()
    return group


@pytest.mark.dependency(depends=["test_create"])
def test_get_by_id(
    group: GroupRepresentation,
):
    """Try getting the previously created group by id by using the fixture"""
    assert group


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create", "test_get_by_id"])
async def test_update_by_id(
    keycloak_admin: KeycloakAdmin, group_id: str, group: GroupRepresentation
):
    """Try updating the previously created group by id"""
    new_group = GroupRepresentation.from_dict(group.to_dict())
    new_group.name = "test_group_updated"
    await keycloak_admin.groups.by_id(group_id).update(new_group)
    updated_group = await keycloak_admin.groups.by_id(group_id).get()
    assert updated_group.name == "test_group_updated"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create", "test_get_by_id", "test_update_by_id"])
async def test_delete_by_id(keycloak_admin: KeycloakAdmin, group_id: str):
    """Try deleting the previously created group by id"""
    await keycloak_admin.groups.by_id(group_id).delete()
    with pytest.raises(Exception, match="404 Not Found"):
        await keycloak_admin.groups.by_id(group_id).get()


# TODO: more tests missing
