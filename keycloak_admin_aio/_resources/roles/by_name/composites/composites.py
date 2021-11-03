from keycloak_admin_aio.types import RoleRepresentation

from .... import KeycloakResource


class RolesByNameComposites(KeycloakResource):
    """Get composites for a role by name.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
        role_name: str
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/composites"

    async def create(self, composite_roles: list[RoleRepresentation]):
        """Create composites for a role by name.

        .. code:: python

            role_representations: list[RoleRepresentation] = []  # needs to be populated
            await kc.roles.by_name(role_name).composites.create(role_representations)
        """
        connection = await self._get_connection()
        await connection.post(
            self.get_url(),
            json=RoleRepresentation.to_dict_list(composite_roles),
        )

    async def get(self) -> list[RoleRepresentation]:
        """Get composites for a role by id.

        .. code:: python

            composites: list[RoleRepresentation] = await kc.roles.by_name(role_name).composites.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_list(response.json())

    async def delete(self, composite_roles: list[RoleRepresentation]):
        """Delete composites for a role by id.

        .. code:: python

            role_representations: list[RoleRepresentation] = []  # needs to be populated
            await kc.roles.by_name(role_name).composites.delete(role_representations)
        """
        connection = await self._get_connection()
        await connection.request(
            method="DELETE",
            url=self.get_url(),
            json=RoleRepresentation.to_dict_list(composite_roles),
        )
