from keycloak_admin_aio.resources import KeycloakResourceWithIdentifier, KeycloakResourcesType
from keycloak_admin_aio.types import RoleRepresentation

from .composites import RolesByNameComposites


class RolesByName(KeycloakResourceWithIdentifier):
    _keycloak_resources: KeycloakResourcesType = [("composites", RolesByNameComposites)]
    composites: RolesByNameComposites

    def get_url(self):
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> RoleRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_dict(response.json())

    async def update(self, role_representation: RoleRepresentation):
        connection = await self._get_connection()
        await connection.put(
            self.get_url(), json=role_representation.to_dict()
        )

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
