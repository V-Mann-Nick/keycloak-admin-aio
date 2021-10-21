from typing import Optional

from keycloak_admin_aio.lib.utils import remove_none
from keycloak_admin_aio.types import UserRepresentation

from .... import KeycloakResource


class GroupsByIdMembers(KeycloakResource):
    def get_url(self):
        return f"{self._get_parent_url()}/members"

    async def get(
        self,
        brief_representation: Optional[bool] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
    ) -> list[UserRepresentation]:
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
