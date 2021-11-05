from keycloak_admin_aio.types import RoleRepresentation

from ... import AttachedResources, KeycloakResourceWithIdentifier
from .composites import RolesByNameComposites


class RolesByName(KeycloakResourceWithIdentifier):
    """Provides roles by name.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
        role_name: str
    """

    _keycloak_resources: AttachedResources = [("composites", RolesByNameComposites)]
    composites: RolesByNameComposites

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> RoleRepresentation:
        """Get role by name.

        .. code:: python

            role: RoleRepresentation = await kc.roles.by_name(role_name).get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return RoleRepresentation.from_dict(response.json())

    async def update(self, role_representation: RoleRepresentation):
        """Update role by name.

        .. code:: python

            role_representation = RoleRepresentation(name="role-name")
            await kc.roles.by_name(role_name).update(role_representation)
        """
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=role_representation.to_dict())

    async def delete(self):
        """Delete role by name.

        .. code:: python

            await kc.roles.by_name(role_name).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
