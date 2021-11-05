from typing import Optional

from keycloak_admin_aio._lib.utils import (
    get_resource_id_in_location_header,
    remove_none,
)
from keycloak_admin_aio.types import GroupRepresentation

from .. import AttachedResources, KeycloakResource, KeycloakResourceWithIdentifierGetter
from .by_id import GroupsById


class Groups(KeycloakResource):
    """Provides the Keycloak group resource

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, GroupRepresentation

        kc: KeycloakAdmin  # must be instantiated
    """

    _keycloak_resources: AttachedResources = [("by_id", GroupsById)]
    by_id: KeycloakResourceWithIdentifierGetter[GroupsById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/groups"

    async def get(
        self,
        brief_representation: Optional[bool] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
        search: Optional[str] = None,
    ) -> list[GroupRepresentation]:
        """Get groups.

        .. code:: python

            groups: list[GroupRepresentation] = await kc.groups.get()
        """
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

    async def create(self, group_representation: GroupRepresentation) -> str:
        """Create a group.

        .. code:: python

            group_representation = GroupRepresentation(name="group-name")
            group_id: str = await kc.groups.create(group_representation)
        """
        connection = await self._get_connection()
        response = await connection.post(
            self.get_url(), json=group_representation.to_dict()
        )
        return get_resource_id_in_location_header(response)

    async def count(
        self, search: Optional[str] = None, top: Optional[bool] = None
    ) -> int:
        """Get group count.

        .. code:: python

            group_count: int = await kc.groups.count()
        """
        connection = await self._get_connection()
        params = remove_none({"search": search, "top": top})
        response = await connection.get(f"{self.get_url()}/count", params=params)
        return response.json()["count"]
