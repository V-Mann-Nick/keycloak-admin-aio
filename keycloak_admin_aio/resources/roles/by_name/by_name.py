from keycloak_admin_aio.resources import KeycloakResource, KeycloakResourcesType

from ..types import RoleRepresentation
from .composites import RolesByNameComposites


class RolesByName(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("composites", RolesByNameComposites)]

    def get_url(self, role_name: str):
        return f"{self._get_parent_url()}/{role_name}"

    async def get(self, role_name: str) -> RoleRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(role_name))
        return RoleRepresentation.from_dict(response.json())

    async def update(self, role_name: str, role_representation: RoleRepresentation):
        connection = await self._get_connection()
        await connection.put(
            self.get_url(role_name), json=role_representation.to_dict()
        )

    async def delete(self, role_name: str):
        connection = await self._get_connection()
        await connection.delete(self.get_url(role_name))
