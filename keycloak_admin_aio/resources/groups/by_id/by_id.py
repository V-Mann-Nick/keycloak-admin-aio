from keycloak_admin_aio.types import GroupRepresentation

from ... import KeycloakResourcesType, KeycloakResourceWithIdentifier
from .children import GroupsByIdChildren
from .members import GroupsByIdMembers


class GroupsById(KeycloakResourceWithIdentifier):
    _keycloak_resources: KeycloakResourcesType = [
        ("children", GroupsByIdChildren),
        ("members", GroupsByIdMembers),
    ]
    children: GroupsByIdChildren
    members: GroupsByIdMembers

    def get_url(self):
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> GroupRepresentation:
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return GroupRepresentation.from_dict(response.json())

    async def update(self, group_representation: GroupRepresentation):
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=group_representation.to_dict())

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
