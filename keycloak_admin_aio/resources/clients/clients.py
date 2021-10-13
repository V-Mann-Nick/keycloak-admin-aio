from typing import Optional

from keycloak_admin_aio.lib.utils import remove_none
from keycloak_admin_aio.types import ClientRepresentation

from .. import (
    KeycloakResource,
    KeycloakResourceWithIdentifierGetter,
    KeycloakResourcesType,
)
from .by_id import ClientsById


class Clients(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("by_id", ClientsById)]
    by_id: KeycloakResourceWithIdentifierGetter[ClientsById]

    def get_url(self):
        return f"{self._get_parent_url()}/clients"

    async def create(self, client_representation: ClientRepresentation):
        connection = await self._get_connection()
        await connection.post(self.get_url(), json=client_representation.to_dict())

    async def get(
        self,
        client_id: Optional[str] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
        q: Optional[str] = None,
        search: Optional[bool] = False,
        viewable_only: Optional[bool] = False,
    ) -> list[ClientRepresentation]:
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
