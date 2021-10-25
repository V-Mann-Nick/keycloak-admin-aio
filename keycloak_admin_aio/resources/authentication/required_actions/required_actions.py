from keycloak_admin_aio.types import RequiredActionProviderRepresentation

from ... import KeycloakResource


class AuthenticationRequiredActions(KeycloakResource):
    def get_url(self):
        return f"{self._get_parent_url()}/required-actions"

    async def get(self) -> list[RequiredActionProviderRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RequiredActionProviderRepresentation.from_list(response.json())
