from keycloak_admin_aio.types import UserRepresentation

from ... import KeycloakResourceWithIdentifier, KeycloakResourcesType
from .role_mappings import UsersByIdRoleMappings
from .groups import UsersByIdGroups


class UsersById(KeycloakResourceWithIdentifier):
    _keycloak_resources: KeycloakResourcesType = [
        ("role_mappings", UsersByIdRoleMappings),
        ("groups", UsersByIdGroups),
    ]
    role_mappings: UsersByIdRoleMappings
    groups: UsersByIdGroups

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self):
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return UserRepresentation.from_dict(response.json())

    async def update(self, user_representation: UserRepresentation):
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=user_representation.to_dict())

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
