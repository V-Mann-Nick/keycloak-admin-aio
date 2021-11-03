from keycloak_admin_aio.types import RoleRepresentation

from ..... import KeycloakResource


class ClientScopesScopeMappingsRealm(KeycloakResource):
    """Realm scope mappings for a client scope by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation

        kc: KeycloakAdmin  # must be instantiated
        client_scope_id: str  # uuid
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/realm"

    async def create(self, role_representations: list[RoleRepresentation]):
        """Add roles to the realm scope mappings of a client scope by id.

        .. code:: python

            role_representations: list[RoleRepresentation] = []  # needs to be populated
            await kc.client_scopes.by_id(client_scope_id).scope_mappings.realm.create(roles)
        """
        connection = await self._get_connection()
        await connection.post(
            self.get_url(),
            json=RoleRepresentation.to_dict_list(role_representations),
        )

    async def get(self) -> list[RoleRepresentation]:
        """Get realm scope mappings for a client scope by id.

        .. code:: python

            client_scope_resource = kc.client_scopes.by_id(client_scope_id)
            roles: list[RoleRepresentation] = await client_scope_resource.scope_mappings.realm.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_list(response.json())

    async def delete(self, role_representations: list[RoleRepresentation]):
        """Remove roles from realm scope mappings for a client scope by id.

        .. code:: python

            role_representations: list[RoleRepresentation] = []  # needs to be populated
            client_scope_resource = kc.client_scopes.by_id(client_scope_id)
            await client_scope_resource.scope_mappings.realm.delete(role_representations)
        """
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(),
            json=RoleRepresentation.to_dict_list(role_representations),
        )
