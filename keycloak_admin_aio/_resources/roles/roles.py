from typing import Optional

from keycloak_admin_aio._lib.utils import (
    get_resource_id_in_location_header,
    remove_none,
)
from keycloak_admin_aio.types import RoleRepresentation

from .. import AttachedResources, KeycloakResource, KeycloakResourceWithIdentifierGetter
from .by_id import RolesById
from .by_name import RolesByName


class Roles(KeycloakResource):
    """Provides the Keycloak role resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, UserRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
    """

    _keycloak_resources: AttachedResources = [
        ("by_id", RolesById),
        ("by_name", RolesByName),
    ]
    by_name: KeycloakResourceWithIdentifierGetter[RolesByName]
    by_id: KeycloakResourceWithIdentifierGetter[RolesById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/roles"

    async def create(self, role_representation: RoleRepresentation) -> str:
        """Create a role.

        .. code:: python

            role_representation = RoleRepresentation(name="some-role")
            role_id: str = await kc.roles.create(role_representation)
        """
        connection = await self._get_connection()
        response = await connection.post(
            self.get_url(), json=role_representation.to_dict()
        )
        role_name = get_resource_id_in_location_header(response, is_no_uuid=True)
        return role_name

    async def get(
        self,
        brief_representation: Optional[bool] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
        search: Optional[str] = None,
    ) -> list[RoleRepresentation]:
        """Get roles.

        .. code:: python

            roles: list[RoleRepresentation] = kc.roles.get()
        """
        connection = await self._get_connection()
        params = remove_none(
            {
                "briefRepresentation": brief_representation,
                "first": first,
                "search": search,
                "max": max,
            }
        )
        response = await connection.get(
            self.get_url(),
            params=params,
        )
        return RoleRepresentation.from_list(response.json())
