from keycloak_admin_aio.types import GroupRepresentation

from .... import KeycloakResource


class GroupsByIdChildren(KeycloakResource):
    def get_url(self):
        return f"{self._get_parent_url()}/children"

    async def add(self, group_representation: GroupRepresentation):
        connection = await self._get_connection()
        await connection.post(self.get_url(), json=group_representation.to_dict())
