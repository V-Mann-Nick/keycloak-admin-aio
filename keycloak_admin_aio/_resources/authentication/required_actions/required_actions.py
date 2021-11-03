from keycloak_admin_aio.types import RequiredActionProviderRepresentation

from ... import KeycloakResource


class AuthenticationRequiredActions(KeycloakResource):
    """Required actions for a realm.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, RequiredActionProviderRepresentation

        kc: KeycloakAdmin  # must be instantiated
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/required-actions"

    async def get(self) -> list[RequiredActionProviderRepresentation]:
        """Get required actions.

        .. code:: python

            required_actions: list[
                RequiredActionProviderRepresentation
            ] = await kc.authentication.required_actions.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RequiredActionProviderRepresentation.from_list(response.json())
