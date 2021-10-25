from keycloak_admin_aio.types import UserRepresentation

from ... import KeycloakResourcesType, KeycloakResourceWithIdentifier
from .execute_actions_email import UsersByIdExecuteActionsEmail
from .groups import UsersByIdGroups
from .role_mappings import UsersByIdRoleMappings


class UsersById(KeycloakResourceWithIdentifier):
    _keycloak_resources: KeycloakResourcesType = [
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
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return UserRepresentation.from_dict(response.json())

    async def update(self, user_representation: UserRepresentation):
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=user_representation.to_dict())

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
