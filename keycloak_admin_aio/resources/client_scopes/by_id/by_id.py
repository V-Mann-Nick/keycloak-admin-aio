from keycloak_admin_aio.types import ClientScopeRepresentation

from ... import KeycloakResourcesType, KeycloakResourceWithIdentifier
from .scope_mappings import ClientScopesScopeMappings


class ClientScopesById(KeycloakResourceWithIdentifier):
    _keycloak_resources: KeycloakResourcesType = [
        ("scope_mappings", ClientScopesScopeMappings)
    ]
    scope_mappings: ClientScopesScopeMappings

    def get_url(self):
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> ClientScopeRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientScopeRepresentation.from_dict(response.json())

    async def update(
        self,
        client_scope_representation: ClientScopeRepresentation,
    ):
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=client_scope_representation.to_dict())

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
