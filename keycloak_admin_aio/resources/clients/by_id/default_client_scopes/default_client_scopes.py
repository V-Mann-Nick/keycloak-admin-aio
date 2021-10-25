from keycloak_admin_aio.resources.keycloak_resource import (
    KeycloakResource,
    KeycloakResourcesType,
    KeycloakResourceWithIdentifierGetter,
)
from keycloak_admin_aio.types import ClientScopeRepresentation

from .by_id import ClientsByIdDefaultClientScopesById


class ClientsByIdDefaultClientScopes(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("by_id", ClientsByIdDefaultClientScopesById)
    ]
    by_id: KeycloakResourceWithIdentifierGetter[ClientsByIdDefaultClientScopesById]

    def get_url(self):
        return f"{self._get_parent_url()}/default-client-scopes"

    async def get(self) -> list[ClientScopeRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientScopeRepresentation.from_list(response.json())
