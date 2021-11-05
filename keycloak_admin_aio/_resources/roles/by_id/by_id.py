from keycloak_admin_aio.types import RoleRepresentation

from ... import AttachedResources, KeycloakResourceWithIdentifier
from .composites import RolesByIdComposites


class RolesById(KeycloakResourceWithIdentifier):
    """Provides roles by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
        role_id: str  # uuid
    """

    _keycloak_resources: AttachedResources = [("composites", RolesByIdComposites)]
    composites: RolesByIdComposites

    def get_url(self) -> str:
        return f"{self._get_parent_url()}-by-id/{self.identifier}"

    async def get(self) -> RoleRepresentation:
        """Get a role by id.

        .. code:: python

            role: RoleRepresentation = await kc.roles.by_id(role_id).get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_dict(response.json())

    async def update(self, role_representation: RoleRepresentation):
        """Update a role by id.

        .. code:: python

            role_representation = RoleRepresentation(name="role-name")
            await kc.roles.by_id(role_id).update(role_representation)
        """
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=role_representation.to_dict())

    async def delete(self):
        """Delete a role by id.

        .. code:: python

            await kc.roles.by_id(role_id).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
