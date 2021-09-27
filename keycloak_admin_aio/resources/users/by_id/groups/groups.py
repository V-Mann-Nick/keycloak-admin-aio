from typing import Optional

from keycloak_admin_aio.lib.utils import remove_none
from keycloak_admin_aio.types import GroupRepresentation

from .... import (
    KeycloakResource,
    KeycloakResourcesType,
    KeycloakResourceWithIdentifierGetter,
)
from .by_id import UsersByIdGroupsById


class UsersByIdGroups(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("by_id", UsersByIdGroupsById)]
    by_id: KeycloakResourceWithIdentifierGetter[UsersByIdGroupsById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/groups"

    async def get(
        self,
        first: Optional[int] = None,
        max: Optional[int] = None,
        search: Optional[str] = None,
        brief_representation: bool = True,
    ):
        connection = await self._get_connection()
        params = remove_none(
            {
                "first": first,
                "max": max,
                "search": search,
                "briefRepresentation": brief_representation,
            }
        )
        response = await connection.get(self.get_url(), params=params)
        return GroupRepresentation.from_dict(response.json())

    async def count(
        self,
        search: Optional[str] = None,
    ) -> int:
        connection = await self._get_connection()
        params = remove_none({"search": search})
        response = await connection.get(self.get_url(), params=params)
        return int(response.json()["count"])
