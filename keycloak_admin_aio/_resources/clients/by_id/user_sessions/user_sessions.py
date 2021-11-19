from typing import Optional

from keycloak_admin_aio._lib.utils import remove_none
from keycloak_admin_aio.types.types import UserSession

from .... import KeycloakResource


class ClientsByIdUserSessions(KeycloakResource):
    """User sessions for clients by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, UserSession

        kc: KeycloakAdmin  # must be instantiated
        client_uuid: str
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/user-sessions"

    async def get(
        self, first: Optional[int] = None, max: Optional[int] = None
    ) -> list[UserSession]:
        """Get user sessions for a client.

        .. code:: python

            user_sessions: lists[UserSession] = await kc.clients.by_id(client_uuid).user_sessions.get()
        """
        connection = await self._get_connection()
        params = remove_none({"first": first, "max": max})
        response = await connection.get(self.get_url(), params=params)
        return UserSession.from_list(response.json())
