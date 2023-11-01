import httpx
import pytest
import pytest_asyncio

from keycloak_admin_aio import KeycloakAdmin
from keycloak_admin_aio.types.types import GroupRepresentation, UserRepresentation

# == keycloak_admin.users ==


@pytest_asyncio.fixture(scope="module")
async def user_id(keycloak_admin: KeycloakAdmin):
    user_id = await keycloak_admin.users.create(
        UserRepresentation(username="test_user")
    )
    return user_id


@pytest.mark.dependency()
def test_create(user_id: str):
    """Create a user by using the fixture"""
    assert user_id


@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_get(keycloak_admin: KeycloakAdmin):
    users = await keycloak_admin.users.get()
    assert len(users) > 0


@pytest.mark.asyncio
async def test_count(keycloak_admin: KeycloakAdmin):
    count = await keycloak_admin.users.count()
    assert count > 0


# == keycloak_admin.users.by_id ==


@pytest_asyncio.fixture(scope="module")
async def user(keycloak_admin: KeycloakAdmin, user_id: str):
    user = await keycloak_admin.users.by_id(user_id).get()
    return user


@pytest.mark.dependency(depends=["test_create"])
def test_get_by_id(
    user: UserRepresentation,
):
    """Try getting the previously created user by id by using the fixture"""
    assert user


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_get_by_id"])
async def test_update_by_id(
    keycloak_admin: KeycloakAdmin, user_id: str, user: UserRepresentation
):
    """Try updating the previously created user by id"""
    new_user = UserRepresentation.from_dict(user.to_dict())
    new_user.email = "test@test.com"
    await keycloak_admin.users.by_id(user_id).update(new_user)
    user = await keycloak_admin.users.by_id(user_id).get()
    assert user.email == "test@test.com"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_update_by_id"])
async def test_delete_by_id(keycloak_admin: KeycloakAdmin, user_id: str):
    """Try deleting the previously created user by id"""
    await keycloak_admin.users.by_id(user_id).delete()
    with pytest.raises(httpx.HTTPStatusError, match="404 Not Found"):
        await keycloak_admin.users.by_id(user_id).get()


# == keycloak_admin.users.by_id.groups & keycloak_admin.users.by_id.groups.by_id ==


@pytest_asyncio.fixture(scope="module")
async def group_id(keycloak_admin: KeycloakAdmin):
    group_id = await keycloak_admin.groups.create(
        GroupRepresentation(name="test_group")
    )
    yield group_id
    await keycloak_admin.groups.by_id(group_id).delete()


@pytest_asyncio.fixture(scope="module")
async def user_2_id(keycloak_admin: KeycloakAdmin, group_id: str):
    user_id = await keycloak_admin.users.create(
        UserRepresentation(username="test_user_2")
    )
    await keycloak_admin.users.by_id(user_id).groups.by_id(group_id).create()
    yield user_id
    await keycloak_admin.users.by_id(user_id).delete()


@pytest.mark.dependency(
    depends=[
        "test/test_users.py::test_create",
        "test/test_users.py::test_delete_by_id",
        "test/test_groups.py::test_create",
        "test/test_groups.py::test_delete_by_id",
    ],
    scope="session",
)
def test_add_to_group(user_2_id: str):
    """Try adding the previously created user to a previously created group by
    asserting the fixture"""
    assert user_2_id


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_add_to_group"])
async def test_get_groups(keycloak_admin: KeycloakAdmin, user_2_id: str):
    """Try getting the groups of the previously created user by id"""
    groups = await keycloak_admin.users.by_id(user_2_id).groups.get()
    assert len(groups) == 1


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_add_to_group"])
async def test_count_groups(keycloak_admin: KeycloakAdmin, user_2_id: str):
    """Try counting the groups of the previously created user by id"""
    count = await keycloak_admin.users.by_id(user_2_id).groups.count()
    assert count == 1


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_add_to_group", "test_count_groups"])
async def test_remove_from_group(
    keycloak_admin: KeycloakAdmin, user_2_id: str, group_id: str
):
    """Try removing the previously created user from the previously created group"""
    await keycloak_admin.users.by_id(user_2_id).groups.by_id(group_id).delete()
    count = await keycloak_admin.users.by_id(user_2_id).groups.count()
    assert count == 0


# == keycloak_admin.users.by_id.role_mappings ==

# TODO
