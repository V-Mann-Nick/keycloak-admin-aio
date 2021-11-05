from keycloak_admin_aio.types import MappingsRepresentation

from .... import AttachedResources, KeycloakResource
from .realm import ClientScopesScopeMappingsRealm


class ClientScopesScopeMappings(KeycloakResource):
    """Scopes mappings for client scopes by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, MappingsRepresentation

        kc: KeycloakAdmin  # must be instantiated
        client_scope_id: str  # uuid
    """

    _keycloak_resources: AttachedResources = [("realm", ClientScopesScopeMappingsRealm)]
    realm: ClientScopesScopeMappingsRealm

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/scope-mappings"

    async def get(self) -> MappingsRepresentation:
        """Get scope mappings for a client scope by id.

        .. code:: python

            client_scope_resource = kc.client_scopes.by_id(client_scope_id)
            mappings: MappingsRepresentation = await client_scope_resource.scope_mappings.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return MappingsRepresentation.from_dict(response.json())
