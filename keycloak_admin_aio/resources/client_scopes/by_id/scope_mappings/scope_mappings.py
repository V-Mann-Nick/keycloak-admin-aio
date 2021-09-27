from keycloak_admin_aio.types import MappingsRepresentation

from .... import KeycloakResource, KeycloakResourcesType
from .realm import ClientScopesScopeMappingsRealm


class ClientScopesScopeMappings(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("realm", ClientScopesScopeMappingsRealm)
    ]
    realm: ClientScopesScopeMappingsRealm

    def get_url(self):
        return f"{self._get_parent_url()}/scope-mappings"

    async def get(self) -> MappingsRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return MappingsRepresentation.from_dict(response.json())
