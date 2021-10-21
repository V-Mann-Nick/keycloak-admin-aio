from typing import Optional

from keycloak_admin_aio.lib.utils import remove_none

from .... import KeycloakResource


class UsersByIdExecuteActionsEmail(KeycloakResource):
    def get_url(self):
        return f"{self._get_parent_url()}/execute-actions-email"

    async def send_email(
        self,
        actions: list[str],
        client_id: Optional[str] = None,
        lifespan: Optional[int] = None,
        redirect_uri: Optional[str] = None,
    ):
        connection = await self._get_connection()
        params = remove_none(
            {"client_id": client_id, "lifespan": lifespan, "redirect_uri": redirect_uri}
        )
        await connection.put(self.get_url(), params=params, json=actions)
