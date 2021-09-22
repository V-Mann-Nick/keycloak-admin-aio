from keycloak_admin_aio.resources.keycloak_resource import KeycloakResourcesType
from keycloak_admin_aio.types import MappingsRepresentation
from .... import KeycloakResource
from .realm import UsersByIdRoleMappingsRealm


class UsersByIdRoleMappings(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("realm", UsersByIdRoleMappingsRealm)]
    realm: UsersByIdRoleMappingsRealm

    def get_url(self, user_id: str) -> str:
        return f"{self._get_parent_url(user_id)}/role-mappings"

    async def get(self, user_id: str) -> MappingsRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url(user_id))
        return MappingsRepresentation.from_dict(response.json())
