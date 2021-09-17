from keycloak_admin_aio.resources import KeycloakResource
from keycloak_admin_aio.types import RoleRepresentation


class RolesByNameComposites(KeycloakResource):
    def get_url(self, role_name: str):
        return f"{self._get_parent_url(role_name)}/composites"

    async def add(self, role_name: str, composite_roles: list[RoleRepresentation]):
        connection = await self._get_connection()
        await connection.post(
            self.get_url(role_name),
            json=RoleRepresentation.to_dict_list(composite_roles),
        )

    async def get(self, role_name: str) -> list[RoleRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(role_name))
        response.raise_for_status()
        return RoleRepresentation.from_list(response.json())

    async def delete(self, role_name: str, composite_roles: list[RoleRepresentation]):
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(role_name),
            json=RoleRepresentation.to_dict_list(composite_roles),
        )
