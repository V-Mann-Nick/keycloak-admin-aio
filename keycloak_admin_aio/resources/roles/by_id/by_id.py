from keycloak_admin_aio.types import RoleRepresentation

from ... import KeycloakResource, KeycloakResourcesType
from .composites import RolesByIdComposites


class RolesById(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("composites", RolesByIdComposites)]
    composites: RolesByIdComposites

    def get_url(self, role_id):
        return f"{self._get_parent_url()}-by-id/{role_id}"

    async def get(self, role_id: str) -> RoleRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(role_id))
        return RoleRepresentation.from_dict(response.json())

    async def update(self, role_id: str, role_representation: RoleRepresentation):
        connection = await self._get_connection()
        await connection.put(self.get_url(role_id), json=role_representation.to_dict())

    async def delete(self, role_id: str):
        connection = await self._get_connection()
        await connection.delete(self.get_url(role_id))
