from keycloak_admin_aio.types import RoleRepresentation

from ..... import KeycloakResource


class ClientScopesScopeMappingsRealm(KeycloakResource):
    def get_url(self, client_scope_id: str):
        return f"{self._get_parent_url(client_scope_id)}/realm"

    async def add(
        self, client_scope_id: str, role_representations: list[RoleRepresentation]
    ):
        connection = await self._get_connection()
        await connection.post(
            self.get_url(client_scope_id),
            json=RoleRepresentation.to_dict_list(role_representations),
        )

    async def get(self, client_scope_id: str) -> list[RoleRepresentation]:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(client_scope_id))
        return RoleRepresentation.from_list(response.json())

    async def delete(
        self, client_scope_id: str, role_representations: list[RoleRepresentation]
    ):
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(client_scope_id),
            json=RoleRepresentation.to_dict_list(role_representations),
        )
