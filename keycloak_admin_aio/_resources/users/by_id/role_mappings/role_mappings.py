from keycloak_admin_aio.types import MappingsRepresentation

from .... import AttachedResources, KeycloakResource
from .realm import UsersByIdRoleMappingsRealm


class UsersByIdRoleMappings(KeycloakResource):
    """Provides the role mappings for a user.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, MappingsRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
        user_id: str  # uuid
    """

    _keycloak_resources: AttachedResources = [("realm", UsersByIdRoleMappingsRealm)]
    realm: UsersByIdRoleMappingsRealm

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/role-mappings"

    async def get(self) -> MappingsRepresentation:
        """Get the role mappings for a user.

        .. code:: python

            mappings: MappingsRepresentation = await kc.users.by_id(user_id).role_mappings.get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return MappingsRepresentation.from_dict(response.json())
