from keycloak_admin_aio.types import ClientScopeRepresentation

from .. import KeycloakResource, KeycloakResourcesType, KeycloakResourceWithIdentifierGetter
from .by_id import ClientScopesById


class ClientScopes(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("by_id", ClientScopesById)]
    by_id: KeycloakResourceWithIdentifierGetter[ClientScopesById]

    def get_url(self):
        return f"{self._get_parent_url()}/client-scopes"

    async def create(self, client_scope_representation: ClientScopeRepresentation):
        connection = await self._get_connection()
        await connection.post(
            self.get_url(), json=client_scope_representation.to_dict()
        )

    async def get(self):
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientScopeRepresentation.from_list(response.json())
