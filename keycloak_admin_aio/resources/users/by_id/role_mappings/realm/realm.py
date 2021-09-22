from keycloak_admin_aio.types import RoleRepresentation

from ..... import KeycloakResource


class UsersByIdRoleMappingsRealm(KeycloakResource):
    def get_url(self, user_id: str) -> str:
        return f"{self._get_parent_url(user_id)}/realm"

    async def get(self, user_id: str) -> list[RoleRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(user_id))
        return RoleRepresentation.from_list(response.json())

    async def create(
        self, user_id: str, role_representations: list[RoleRepresentation]
    ):
        connection = await self._get_connection()
        await connection.post(
            self.get_url(user_id),
            json=RoleRepresentation.to_dict_list(role_representations),
        )

    async def delete(
        self, user_id: str, role_representations: list[RoleRepresentation]
    ):
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(user_id),
            json=RoleRepresentation.to_dict_list(role_representations),
        )

    async def available(self, user_id: str) -> list[RoleRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(f"{self.get_url(user_id)}/available")
        return RoleRepresentation.from_list(response.json())
