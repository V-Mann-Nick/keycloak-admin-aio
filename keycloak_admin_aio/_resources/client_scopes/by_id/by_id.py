from keycloak_admin_aio.types import ClientScopeRepresentation

from ... import AttachedResources, KeycloakResourceWithIdentifier
from .scope_mappings import ClientScopesScopeMappings


class ClientScopesById(KeycloakResourceWithIdentifier):
    """Client scopes by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, ClientScopeRepresentation

        kc: KeycloakAdmin  # must be instantiated
        client_scope_id: str  # uuid
    """

    _keycloak_resources: AttachedResources = [
        ("scope_mappings", ClientScopesScopeMappings)
    ]
    scope_mappings: ClientScopesScopeMappings

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> ClientScopeRepresentation:
        """Get a client scope by id.

        .. code:: python

            client_scope: ClientScopeRepresentation = await kc.client_scopes.by_id(client_scope_id).get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientScopeRepresentation.from_dict(response.json())

    async def update(
        self,
        client_scope_representation: ClientScopeRepresentation,
    ):
        """Update a client scope by id.

        .. code:: python

            client_scope_representation = ClientScopeRepresentation(name="client-scope-name")
            await kc.client_scopes.by_id(client_scope_id).update(client_scope_representation)
        """
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=client_scope_representation.to_dict())

    async def delete(self):
        """Delete a client scope by id.

        .. code:: python

            await kc.client_scopes.by_id(client_scope_id).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
