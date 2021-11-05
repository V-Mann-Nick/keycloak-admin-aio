from ..... import KeycloakResourceWithIdentifier


class ClientsByIdDefaultClientScopesById(KeycloakResourceWithIdentifier):
    """Client scopes by id for a client by UUID.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin

        kc: KeycloakAdmin  # must be instantiated
        client_uuid: str
        client_scope_id: str  # uuid
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def create(self):
        """Add a client scope by id to a client by id.

        .. code:: python

            await kc.clients.by_id(client_uuid).default_client_scopes.by_id(client_scope_id).add()
        """
        connection = await self._get_connection()
        await connection.put(self.get_url())

    async def delete(self):
        """Remove a client scope by id from a client by id.

        .. code:: python

            await kc.clients.by_id(client_uuid).default_client_scopes.by_id(client_scope_id).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
