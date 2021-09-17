from keycloak_admin_aio.resources.keycloak_resource import KeycloakResourcesType
from keycloak_admin_aio.types import ClientScopeRepresentation

from ... import KeycloakResource
from .scope_mappings import ClientScopesScopeMappings


class ClientScopesById(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("scope_mappings", ClientScopesScopeMappings)
    ]
    scope_mappings: ClientScopesScopeMappings

    def get_url(self, client_scope_id: str):
        return f"{self._get_parent_url()}/{client_scope_id}"

    async def get(self, client_scope_id: str) -> ClientScopeRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(client_scope_id))
        return ClientScopeRepresentation.from_dict(response.json())

    async def update(
        self,
        client_scope_id: str,
        client_scope_representation: ClientScopeRepresentation,
    ):
        connection = await self._get_connection()
        await connection.put(
            self.get_url(client_scope_id), json=client_scope_representation.to_dict()
        )

    async def delete(self, client_scope_id: str):
        connection = await self._get_connection()
        await connection.delete(self.get_url(client_scope_id))
