from keycloak_admin_aio.resources.keycloak_resource import KeycloakResourcesType
from keycloak_admin_aio.types import UserRepresentation

from ... import KeycloakResource
from .role_mappings import UsersByIdRoleMappings
from .groups import UsersByIdGroups


class UsersById(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("role_mappings", UsersByIdRoleMappings),
        ("groups", UsersByIdGroups)
    ]
    role_mappings: UsersByIdRoleMappings
    groups: UsersByIdGroups

    def get_url(self, user_id: str) -> str:
        return f"{self._get_parent_url()}/{user_id}"

    async def get(self, user_id: str):
        connection = await self._get_connection()
        response = await connection.get(self.get_url(user_id))
        return UserRepresentation.from_dict(response.json())

    async def update(self, user_id: str, user_representation: UserRepresentation):
        connection = await self._get_connection()
        await connection.put(self.get_url(user_id), json=user_representation.to_dict())

    async def delete(self, user_id: str):
        connection = await self._get_connection()
        await connection.delete(self.get_url(user_id))
