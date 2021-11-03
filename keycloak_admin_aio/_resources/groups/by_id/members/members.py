from typing import Optional

from keycloak_admin_aio._lib.utils import remove_none
from keycloak_admin_aio.types import UserRepresentation

from .... import KeycloakResource


class GroupsByIdMembers(KeycloakResource):
    """Members of groups by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, UserRepresentation

        kc: KeycloakAdmin  # must be instantiated
        group_id: str  # uuid
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/members"

    async def get(
        self,
        brief_representation: Optional[bool] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
    ) -> list[UserRepresentation]:
        """Get members of a group by id.

        .. code:: python

            members: list[UserRepresentation] = await kc.groups.by_id(group_id).members.get()
        """
        connection = await self._get_connection()
        params = remove_none(
            {
                "briefRepresentation": brief_representation,
                "first": first,
                "max": max,
            }
        )
        response = await connection.get(self.get_url(), params=params)
        return UserRepresentation.from_list(response.json())
