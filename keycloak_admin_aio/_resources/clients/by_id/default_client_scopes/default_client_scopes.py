from keycloak_admin_aio.types import ClientScopeRepresentation

from .... import (
    AttachedResources,
    KeycloakResource,
    KeycloakResourceWithIdentifierGetter,
)
from .by_id import ClientsByIdDefaultClientScopesById


class ClientsByIdDefaultClientScopes(KeycloakResource):
    """Default client scopes for clients by UUID.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, ClientScopeRepresentation

        kc: KeycloakAdmin  # must be instantiated
        client_uuid: str
    """

    _keycloak_resources: AttachedResources = [
        ("by_id", ClientsByIdDefaultClientScopesById)
    ]
    by_id: KeycloakResourceWithIdentifierGetter[ClientsByIdDefaultClientScopesById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/default-client-scopes"

    async def get(self) -> list[ClientScopeRepresentation]:
        """Get default clients scopes for a client by UUID.

        .. code:: python

            client_scope_resource = kc.clients.by_id(client_uuid)
            client_scope_representations: list[
                ClientScopeRepresentation
            ] = await client_scope_resource.default_client_scopes.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientScopeRepresentation.from_list(response.json())
