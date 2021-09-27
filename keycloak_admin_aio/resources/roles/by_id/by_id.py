from keycloak_admin_aio.types import RoleRepresentation

from ... import KeycloakResourcesType, KeycloakResourceWithIdentifier
from .composites import RolesByIdComposites


class RolesById(KeycloakResourceWithIdentifier):
    _keycloak_resources: KeycloakResourcesType = [("composites", RolesByIdComposites)]
    composites: RolesByIdComposites

    def get_url(self):
        return f"{self._get_parent_url()}-by-id/{self.identifier}"

    async def get(self) -> RoleRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_dict(response.json())

    async def update(self, role_representation: RoleRepresentation):
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=role_representation.to_dict())

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
