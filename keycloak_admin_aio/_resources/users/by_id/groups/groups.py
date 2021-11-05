from typing import Optional

from keycloak_admin_aio._lib.utils import remove_none
from keycloak_admin_aio.types import GroupRepresentation

from .... import (
    AttachedResources,
    KeycloakResource,
    KeycloakResourceWithIdentifierGetter,
)
from .by_id import UsersByIdGroupsById


class UsersByIdGroups(KeycloakResource):
    """Provides the Keycloak groups resource for users by id

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, GroupRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
        user_id: str  # uuid
    """

    _keycloak_resources: AttachedResources = [("by_id", UsersByIdGroupsById)]
    by_id: KeycloakResourceWithIdentifierGetter[UsersByIdGroupsById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/groups"

    async def get(
        self,
        first: Optional[int] = None,
        max: Optional[int] = None,
        search: Optional[str] = None,
        brief_representation: bool = True,
    ) -> list[GroupRepresentation]:
        """Get the user's groups.

        .. code:: python

            groups: list[GroupRepresentation] = await kc.users.by_id(user_id).groups.get()
        """
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
        return GroupRepresentation.from_list(response.json())

    async def count(
        self,
        search: Optional[str] = None,
    ) -> int:
        """Get the number of groups the user belongs to.

        .. code:: python

            membership_count: int = await kc.users.by_id(user_id).groups.count()
        """
        connection = await self._get_connection()
        params = remove_none({"search": search})
        response = await connection.get(self.get_url(), params=params)
        return int(response.json()["count"])
