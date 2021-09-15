from typing import Optional

from keycloak_admin_aio.lib.utils import remove_none

from .. import KeycloakResource, KeycloakResourcesType
from .by_id import RolesById
from .by_name import RolesByName
from .types import RoleRepresentation


class Roles(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("by_name", RolesByName),
        ("by_id", RolesById),
    ]

    def get_url(self):
        return f"{self._get_parent_url()}/roles"

    async def create(self, role_representation: RoleRepresentation):
        connection = await self._get_connection()
        await connection.post(self.get_url(), json=role_representation.to_dict())

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
