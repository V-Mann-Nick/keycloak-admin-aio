from .by_id import GroupsById
from keycloak_admin_aio.resources.keycloak_resource import (
    KeycloakResourceWithIdentifierGetter,
    KeycloakResourcesType,
)
from keycloak_admin_aio.lib.utils import get_resource_id_in_location_header, remove_none
from keycloak_admin_aio.types import GroupRepresentation
from typing import Optional
from .. import KeycloakResource


class Groups(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("by_id", GroupsById)]
    by_id: KeycloakResourceWithIdentifierGetter[GroupsById]

    def get_url(self):
        return f"{self._get_parent_url()}/groups"

    async def get(
        self,
        brief_representation: Optional[bool] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
        search: Optional[str] = None,
    ) -> list[GroupRepresentation]:
        connection = await self._get_connection()
        params = remove_none(
            {
                "briefRepresentation": brief_representation,
                "first": first,
                "max": max,
                "search": search,
            }
        )
        response = await connection.get(self.get_url(), params=params)
        return GroupRepresentation.from_list(response.json())

    async def create(self, group_representation: GroupRepresentation):
        connection = await self._get_connection()
        response = await connection.post(self.get_url(), json=group_representation.to_dict())
        return get_resource_id_in_location_header(response)

    async def count(
        self, search: Optional[str] = None, top: Optional[bool] = None
    ) -> int:
        connection = await self._get_connection()
        params = remove_none({"search": search, "top": top})
        response = await connection.get(f"{self.get_url()}/count", params=params)
        return response.json()["count"]
