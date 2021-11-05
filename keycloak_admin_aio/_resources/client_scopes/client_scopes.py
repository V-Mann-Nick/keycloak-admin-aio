from keycloak_admin_aio._lib.utils import get_resource_id_in_location_header
from keycloak_admin_aio.types import ClientScopeRepresentation

from .. import AttachedResources, KeycloakResource, KeycloakResourceWithIdentifierGetter
from .by_id import ClientScopesById


class ClientScopes(KeycloakResource):
    """Provides the Keycloak client scopes resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, ClientScopeRepresentation

        kc: KeycloakAdmin  # must be instantiated
    """

    _keycloak_resources: AttachedResources = [("by_id", ClientScopesById)]
    by_id: KeycloakResourceWithIdentifierGetter[ClientScopesById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/client-scopes"

    async def create(
        self, client_scope_representation: ClientScopeRepresentation
    ) -> str:
        """Create a client scope.

        .. code:: python

            client_scope_representation = ClientScopeRepresentation(name="client-scope-name")
            client_scope_id: str = await kc.client_scopes.create(client_scope_representation)
        """
        connection = await self._get_connection()
        response = await connection.post(
            self.get_url(), json=client_scope_representation.to_dict()
        )
        return get_resource_id_in_location_header(response)

    async def get(self):
        """Get client scopes.

        .. code:: python

            client_scopes: list[ClientScopeRepresentation] = await kc.client_scopes.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientScopeRepresentation.from_list(response.json())
