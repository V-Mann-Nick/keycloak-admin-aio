import asyncio

import httpx
import pytest
import pytest_asyncio

from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation
from keycloak_admin_aio._lib.utils import cast_non_optional


@pytest.fixture
def role_representation():
    return RoleRepresentation(name="test-role")


@pytest.fixture
def role_representation2():
    return RoleRepresentation(name="test-role-2")


@pytest_asyncio.fixture
async def test_role(
    keycloak_admin: KeycloakAdmin, role_representation: RoleRepresentation
):
    yield role_representation
    await keycloak_admin.roles.by_name(
        cast_non_optional(role_representation.name)
    ).delete()


@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_create(keycloak_admin: KeycloakAdmin, test_role: RoleRepresentation):
    role_name = await keycloak_admin.roles.create(test_role)
    assert test_role.name == role_name


@pytest.mark.asyncio
async def test_get(keycloak_admin: KeycloakAdmin):
    assert await keycloak_admin.roles.get()


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create"])
async def test_roles_by_name(
    keycloak_admin: KeycloakAdmin, role_representation: RoleRepresentation
):
    role_name = cast_non_optional(role_representation.name)
    assert await keycloak_admin.roles.create(role_representation)
    updated_role = RoleRepresentation(name=role_name, description="Description")
    await keycloak_admin.roles.by_name(role_name).update(updated_role)
    inserted_role = await keycloak_admin.roles.by_name(role_name).get()
    assert inserted_role.description == updated_role.description
    await keycloak_admin.roles.by_name(role_name).delete()
    with pytest.raises(httpx.HTTPStatusError, match="404 Not Found"):
        await keycloak_admin.roles.by_name(role_name).get()


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create"])
async def test_roles_by_id(
    keycloak_admin: KeycloakAdmin, role_representation: RoleRepresentation
):
    role_name = cast_non_optional(role_representation.name)
    assert await keycloak_admin.roles.create(role_representation)
    full_representation = await keycloak_admin.roles.by_name(role_name).get()
    role_id = cast_non_optional(full_representation.id)
    updated_role = RoleRepresentation(name=role_name, description="Description")
    await keycloak_admin.roles.by_id(role_id).update(updated_role)
    inserted_role = await keycloak_admin.roles.by_id(role_id).get()
    assert inserted_role.description == updated_role.description
    await keycloak_admin.roles.by_id(role_id).delete()
    with pytest.raises(httpx.HTTPStatusError, match="404 Not Found"):
        await keycloak_admin.roles.by_id(role_id).get()


@pytest_asyncio.fixture
async def test_roles(
    keycloak_admin: KeycloakAdmin,
    role_representation: RoleRepresentation,
    role_representation2: RoleRepresentation,
):
    await asyncio.gather(
        keycloak_admin.roles.create(role_representation),
        keycloak_admin.roles.create(role_representation2),
    )
    full_representation1, full_representation2 = await asyncio.gather(
        keycloak_admin.roles.by_name(cast_non_optional(role_representation.name)).get(),
        keycloak_admin.roles.by_name(
            cast_non_optional(role_representation2.name)
        ).get(),
    )
    yield full_representation1, full_representation2
    await asyncio.gather(
        keycloak_admin.roles.by_name(
            cast_non_optional(role_representation.name)
        ).delete(),
        keycloak_admin.roles.by_name(
            cast_non_optional(role_representation2.name)
        ).delete(),
    )


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_roles_by_name"])
async def test_composite_roles_by_name(
    keycloak_admin: KeycloakAdmin,
    test_roles: tuple[RoleRepresentation, RoleRepresentation],
):
    role_representation1, role_representation2 = test_roles
    role_name = cast_non_optional(role_representation1.name)
    await keycloak_admin.roles.by_name(role_name).composites.create(
        [role_representation2]
    )
    composites = await keycloak_admin.roles.by_name(role_name).composites.get()
    assert len(composites) == 1 and composites[0].name == role_representation2.name
    await keycloak_admin.roles.by_name(role_name).composites.delete(
        [role_representation2]
    )
    composites = await keycloak_admin.roles.by_name(role_name).composites.get()
    assert len(composites) == 0


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_roles_by_id"])
async def test_composite_roles_by_id(
    keycloak_admin: KeycloakAdmin,
    test_roles: tuple[RoleRepresentation, RoleRepresentation],
):
    role_representation1, role_representation2 = test_roles
    role_id = cast_non_optional(role_representation1.id)
    await keycloak_admin.roles.by_id(role_id).composites.create([role_representation2])
    composites = await keycloak_admin.roles.by_id(role_id).composites.get()
    assert len(composites) == 1 and composites[0].name == role_representation2.name
    await keycloak_admin.roles.by_id(role_id).composites.delete([role_representation2])
    composites = await keycloak_admin.roles.by_id(role_id).composites.get()
    assert len(composites) == 0
