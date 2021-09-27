from keycloak_admin_aio.types import RoleRepresentation

from ..... import KeycloakResource


class ClientScopesScopeMappingsRealm(KeycloakResource):
    def get_url(self):
        return f"{self._get_parent_url()}/realm"

    async def create(self, role_representations: list[RoleRepresentation]):
        connection = await self._get_connection()
        await connection.post(
            self.get_url(),
            json=RoleRepresentation.to_dict_list(role_representations),
        )

    async def get(self) -> list[RoleRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_list(response.json())

    async def delete(
        self, role_representations: list[RoleRepresentation]
    ):
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(),
            json=RoleRepresentation.to_dict_list(role_representations),
        )
