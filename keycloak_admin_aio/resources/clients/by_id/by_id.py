from keycloak_admin_aio.types import ClientRepresentation

from ... import KeycloakResourcesType, KeycloakResourceWithIdentifier
from .default_client_scopes import ClientsByIdDefaultClientScopes


class ClientsById(KeycloakResourceWithIdentifier):
    _keycloak_resources: KeycloakResourcesType = [
        ("default_client_scopes", ClientsByIdDefaultClientScopes)
    ]
    default_client_scopes: ClientsByIdDefaultClientScopes

    def get_url(self):
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> ClientRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientRepresentation.from_dict(response.json())

    async def update(self, client_representation: ClientRepresentation):
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=client_representation.to_dict())

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
