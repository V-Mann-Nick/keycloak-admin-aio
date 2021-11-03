from typing import Optional

from keycloak_admin_aio.lib.utils import get_resource_id_in_location_header, remove_none
from keycloak_admin_aio.resources.keycloak_resource import (
    KeycloakResourceWithIdentifierGetter,
)
from keycloak_admin_aio.types import RoleRepresentation

from .. import KeycloakResource, KeycloakResourcesType
from .by_id import RolesById
from .by_name import RolesByName


class Roles(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("by_id", RolesById),
        ("by_name", RolesByName),
    ]
    by_name: KeycloakResourceWithIdentifierGetter[RolesByName]
    by_id: KeycloakResourceWithIdentifierGetter[RolesById]

    def get_url(self):
        return f"{self._get_parent_url()}/roles"

    async def create(self, role_representation: RoleRepresentation) -> str:
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
