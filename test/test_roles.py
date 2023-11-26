import asyncio
from typing import Literal, Union

import pytest
from dependencies_plugin import depends
from utils import ResourceLifeCycleTest, assert_not_raises

from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation
from keycloak_admin_aio._lib.utils import cast_non_optional
from keycloak_admin_aio._resources.roles.by_id.composites.composites import (
    RolesByIdComposites,
)
from keycloak_admin_aio._resources.roles.by_name.composites.composites import (
    RolesByNameComposites,
)


@assert_not_raises
async def test_get(keycloak_admin: KeycloakAdmin):
    """Test keycloak_admin.roles.get"""
    await keycloak_admin.roles.get()


class TestByNameLifeCycle(ResourceLifeCycleTest):
    """Test keycloak_admin.roles & keycloak_admin.roles.by_name"""

    @pytest.fixture(scope="class")
    def create(self, keycloak_admin: KeycloakAdmin):
        async def create():
            return await keycloak_admin.roles.create(RoleRepresentation(name="test"))

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin):
        async def get(role_name: str):
            return await keycloak_admin.roles.by_name(role_name).get()

        return get

    @pytest.fixture(scope="class")
    def update(self, keycloak_admin: KeycloakAdmin):
        async def update(role_name: str):
            await keycloak_admin.roles.by_name(role_name).update(
                RoleRepresentation(name="test", description="test")
            )

        return update

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin):
        async def delete(role_name: str):
            await keycloak_admin.roles.by_name(role_name).delete()

        return delete


@depends(on=[TestByNameLifeCycle.dependency_name("get")])
class TestByIdLifeCycle(ResourceLifeCycleTest):
    """Test keycloak_admin.roles & keycloak_admin.roles.by_id"""

    @pytest.fixture(scope="class")
    def create(self, keycloak_admin: KeycloakAdmin):
        async def create():
            role_name = await keycloak_admin.roles.create(
                RoleRepresentation(name="test")
            )
            role = await keycloak_admin.roles.by_name(role_name).get()
            return cast_non_optional(role.id)

        return create

    @pytest.fixture(scope="class")
    def get(self, keycloak_admin: KeycloakAdmin):
        async def get(role_id: str):
            return await keycloak_admin.roles.by_id(role_id).get()

        return get

    @pytest.fixture(scope="class")
    def update(self, keycloak_admin: KeycloakAdmin):
        async def update(role_id: str):
            await keycloak_admin.roles.by_id(role_id).update(
                RoleRepresentation(name="test", description="test")
            )

        return update

    @pytest.fixture(scope="class")
    def delete(self, keycloak_admin: KeycloakAdmin):
        async def delete(role_id: str):
            await keycloak_admin.roles.by_id(role_id).delete()

        return delete


class TestRoleComposites:
    """Test keycloak_admin.roles.by_name.composites & keycloak_admin.roles.by_id.composites"""

    DEPENDENCIES = [
        TestByNameLifeCycle.dependency_name("create"),
        TestByNameLifeCycle.dependency_name("get"),
        TestByNameLifeCycle.dependency_name("delete"),
    ]

    @pytest.fixture(scope="class")
    async def roles(self, keycloak_admin: KeycloakAdmin):
        role_name, role_name_2 = "test", "test2"
        await asyncio.gather(
            keycloak_admin.roles.create(RoleRepresentation(name=role_name)),
            keycloak_admin.roles.create(RoleRepresentation(name=role_name_2)),
        )
        role, role_2 = await asyncio.gather(
            keycloak_admin.roles.by_name(role_name).get(),
            keycloak_admin.roles.by_name(role_name_2).get(),
        )
        yield role, role_2
        await asyncio.gather(
            keycloak_admin.roles.by_name(role_name).delete(),
            keycloak_admin.roles.by_name(role_name_2).delete(),
        )

    @pytest.fixture(scope="class", params=["by_name", "by_id"])
    async def composite_class(self, request):
        yield request.param

    def get_composite_class(
        self,
        keycloak_admin: KeycloakAdmin,
        composite_class: Literal["by_name", "by_id"],
        role: RoleRepresentation,
    ) -> Union[RolesByIdComposites, RolesByNameComposites]:
        identifier = cast_non_optional(
            role.id if composite_class == "by_id" else role.name
        )
        return getattr(keycloak_admin.roles, composite_class)(identifier).composites

    @depends(on=DEPENDENCIES)
    @assert_not_raises
    async def test_create(
        self,
        keycloak_admin: KeycloakAdmin,
        roles: tuple[RoleRepresentation, RoleRepresentation],
        composite_class: Literal["by_name", "by_id"],
    ):
        role, role_2 = roles
        await self.get_composite_class(keycloak_admin, composite_class, role).create(
            [role_2]
        )

    @depends(on=DEPENDENCIES)
    @assert_not_raises
    async def test_get(
        self,
        keycloak_admin: KeycloakAdmin,
        roles: tuple[RoleRepresentation, RoleRepresentation],
        composite_class: Literal["by_name", "by_id"],
    ):
        # FIXME
        # depends(request, [f"test_create[{composite_class}]"], scope="class")
        role, role_2 = roles
        composites = await self.get_composite_class(
            keycloak_admin, composite_class, role
        ).get()
        assert len(composites) == 1 and composites[0].name == role_2.name

    @depends(on=DEPENDENCIES)
    @assert_not_raises
    async def test_delete(
        self,
        keycloak_admin: KeycloakAdmin,
        roles: tuple[RoleRepresentation, RoleRepresentation],
        composite_class: Literal["by_name", "by_id"],
    ):
        # FIXME
        # depends(request, [f"test_get[{composite_class}]"], scope="class")
        role, role_2 = roles
        await self.get_composite_class(keycloak_admin, composite_class, role).delete(
            [role_2]
        )
        composites = await self.get_composite_class(
            keycloak_admin, composite_class, role
        ).get()
        assert len(composites) == 0
