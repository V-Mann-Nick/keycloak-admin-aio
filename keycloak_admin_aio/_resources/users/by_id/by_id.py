from keycloak_admin_aio.types import UserRepresentation

from ... import AttachedResources, KeycloakResourceWithIdentifier
from .execute_actions_email import UsersByIdExecuteActionsEmail
from .groups import UsersByIdGroups
from .role_mappings import UsersByIdRoleMappings


class UsersById(KeycloakResourceWithIdentifier):
    """Provides the Keycloak users by id resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, UserRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
        user_id: str  # uuid
    """

    _keycloak_resources: AttachedResources = [
        ("role_mappings", UsersByIdRoleMappings),
        ("groups", UsersByIdGroups),
        ("execute_actions_email", UsersByIdExecuteActionsEmail),
    ]
    role_mappings: UsersByIdRoleMappings
    groups: UsersByIdGroups
    execute_actions_email: UsersByIdExecuteActionsEmail

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> UserRepresentation:
        """Get user by id.

        .. code:: python

            user: UserRepresentation = await kc.users.by_id(user_id).get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return UserRepresentation.from_dict(response.json())

    async def update(self, user_representation: UserRepresentation):
        """Update user by id.

        .. code:: python

            user_representation = UserRepresentation(first_name="New name")
            await kc.users.by_id(user_id).update(user_representation)
        """
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=user_representation.to_dict())

    async def delete(self):
        """Delete user by id.

        .. code:: python

            await kc.users.by_id(user_id).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
