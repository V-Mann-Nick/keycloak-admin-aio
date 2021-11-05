from typing import Optional

from keycloak_admin_aio._lib.utils import (
    get_resource_id_in_location_header,
    remove_none,
)
from keycloak_admin_aio.types import ClientRepresentation

from .. import AttachedResources, KeycloakResource, KeycloakResourceWithIdentifierGetter
from .by_id import ClientsById


class Clients(KeycloakResource):
    """Provides the Keycloak clients resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, ClientRepresentation

        kc: KeycloakAdmin  # must be instantiated
    """

    _keycloak_resources: AttachedResources = [("by_id", ClientsById)]
    by_id: KeycloakResourceWithIdentifierGetter[ClientsById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/clients"

    async def create(self, client_representation: ClientRepresentation) -> str:
        """Create a client.

        .. code:: python

            client_representation = ClientRepresentation(name="client-name")
            client_uuid: str = await kc.clients.create(client_representation)
        """
        connection = await self._get_connection()
        response = await connection.post(
            self.get_url(), json=client_representation.to_dict()
        )
        return get_resource_id_in_location_header(response)

    async def get(
        self,
        client_id: Optional[str] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
        q: Optional[str] = None,
        search: Optional[bool] = False,
        viewable_only: Optional[bool] = False,
    ) -> list[ClientRepresentation]:
        """Get clients.

        .. code:: python

            clients: list[ClientRepresentation] = await kc.clients.get()
        """
        connection = await self._get_connection()
        params = remove_none(
            {
                "clientId": client_id,
                "first": first,
                "max": max,
                "q": q,
                "search": search,
                "viewableOnly": viewable_only,
            }
        )
        response = await connection.get(self.get_url(), params=params)
        return ClientRepresentation.from_list(response.json())
