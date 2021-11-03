from typing import Optional

from keycloak_admin_aio._lib.utils import remove_none

from .... import KeycloakResource


class UsersByIdExecuteActionsEmail(KeycloakResource):
    """Provides the Keycloak user execute actions email resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin

        kc: KeycloakAdmin  # needs to be instantiated
        user_id: str
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/execute-actions-email"

    async def send_email(
        self,
        actions: list[str],
        client_id: Optional[str] = None,
        lifespan: Optional[int] = None,
        redirect_uri: Optional[str] = None,
    ):
        """Send email to user.

        .. code:: python

            await kc.users.by_id(user_id).execute_actions_email.send_email()
        """
        connection = await self._get_connection()
        params = remove_none(
            {"client_id": client_id, "lifespan": lifespan, "redirect_uri": redirect_uri}
        )
        await connection.put(self.get_url(), params=params, json=actions)
