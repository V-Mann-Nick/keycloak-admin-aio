from keycloak_admin_aio.types import RoleRepresentation

from ..... import KeycloakResource


class UsersByIdRoleMappingsRealm(KeycloakResource):
    """Provides the realm role mappings for users.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
        user_id: str  # uuid
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/realm"

    async def get(self) -> list[RoleRepresentation]:
        """Get realm role mappings for a user.

        .. code:: python

            roles: list[RoleRepresentation] = await kc.users.by_id(user_id).role_mappings.realm.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_list(response.json())

    async def create(self, role_representations: list[RoleRepresentation]):
        """Create realm role mappings for a user.

        .. code:: python

            roles list[RoleRepresentation] = []  # needs to be populated
            await kc.users.by_id(user_id).role_mappings.realm.create(roles)
        """
        connection = await self._get_connection()
        await connection.post(
            self.get_url(),
            json=RoleRepresentation.to_dict_list(role_representations),
        )

    async def delete(self, role_representations: list[RoleRepresentation]):
        """Delete realm roles mappings for a user.

        .. code:: python

            roles: list[RoleRepresentation] = []  # needs to be populated
            await kc.users.by_id(user_id).role_mappings.realm.delete(roles)
        """
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(),
            json=RoleRepresentation.to_dict_list(role_representations),
        )

    async def available(self) -> list[RoleRepresentation]:
        """Get available roles which can be mapped to the user.

        .. code:: python

            roles: list[RoleRepresentation] = await kc.users.by_id(user_id).role_mappings.realm.available()
        """
        connection = await self._get_connection()
        response = await connection.get(f"{self.get_url()}/available")
        return RoleRepresentation.from_list(response.json())

    async def composite(self) -> list[RoleRepresentation]:
        """Get composed realm roles for a user.

        .. code:: python

            roles: list[RoleRepresentation] = await kc.users.by_id(user_id).role_mappings.realm.composite()
        """

        connection = await self._get_connection()
        response = await connection.get(f"{self.get_url()}/composite")
        return RoleRepresentation.from_list(response.json())
