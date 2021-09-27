from keycloak_admin_aio.resources import KeycloakResource
from keycloak_admin_aio.types import RoleRepresentation


class RolesByNameComposites(KeycloakResource):
    def get_url(self):
        return f"{self._get_parent_url()}/composites"

    async def create(self, composite_roles: list[RoleRepresentation]):
        connection = await self._get_connection()
        await connection.post(
            self.get_url(),
            json=RoleRepresentation.to_dict_list(composite_roles),
        )

    async def get(self) -> list[RoleRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_list(response.json())

    async def delete(self, composite_roles: list[RoleRepresentation]):
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(),
            json=RoleRepresentation.to_dict_list(composite_roles),
        )
