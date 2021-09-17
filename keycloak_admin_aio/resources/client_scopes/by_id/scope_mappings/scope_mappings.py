from keycloak_admin_aio.resources.keycloak_resource import KeycloakResourcesType
from keycloak_admin_aio.types import MappingsRepresentation

from .... import KeycloakResource
from .realm import ClientScopesScopeMappingsRealm


class ClientScopesScopeMappings(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("realm", ClientScopesScopeMappingsRealm)
    ]
    realm: ClientScopesScopeMappingsRealm

    def get_url(self, client_scope_id: str):
        return f"{self._get_parent_url(client_scope_id)}/scope-mappings"

    async def get(self, client_scope_id: str) -> MappingsRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(client_scope_id))
        return MappingsRepresentation.from_dict(response.json())
