from keycloak_admin_aio.types import ClientRepresentation

from ... import AttachedResources, KeycloakResourceWithIdentifier
from .default_client_scopes import ClientsByIdDefaultClientScopes
from .user_sessions import ClientsByIdUserSessions


class ClientsById(KeycloakResourceWithIdentifier):
    """Clients by UUID.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, ClientRepresentation

        kc: KeycloakAdmin  # must be instantiated
        client_uuid: str
    """

    _keycloak_resources: AttachedResources = [
        ("default_client_scopes", ClientsByIdDefaultClientScopes),
        ("user_sessions", ClientsByIdUserSessions),
    ]
    default_client_scopes: ClientsByIdDefaultClientScopes
    user_sessions: ClientsByIdUserSessions

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> ClientRepresentation:
        """Get a client by UUID.

        .. code:: python

            client_representation: ClientRepresentation = await kc.clients.by_id(client_uuid).get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return ClientRepresentation.from_dict(response.json())

    async def update(self, client_representation: ClientRepresentation):
        """Update a client by UUID.

        .. code:: python

            client_representation = ClientRepresentation(name="client-name")
            await kc.clients.by_id(client_uuid).update(client_representation)
        """
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=client_representation.to_dict())

    async def delete(self):
        """Delete a client by UUID.

        .. code:: python

            await kc.clients.by_id(client_uuid).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
