from keycloak_admin_aio.types import GroupRepresentation

from ... import AttachedResources, KeycloakResourceWithIdentifier
from .children import GroupsByIdChildren
from .members import GroupsByIdMembers


class GroupsById(KeycloakResourceWithIdentifier):
    """Groups by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, GroupRepresentation

        kc: KeycloakAdmin  # must be instantiated
        group_id: str  # uuid
    """

    _keycloak_resources: AttachedResources = [
        ("children", GroupsByIdChildren),
        ("members", GroupsByIdMembers),
    ]
    children: GroupsByIdChildren
    members: GroupsByIdMembers

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> GroupRepresentation:
        """Get a group by id.

        .. code:: python

            group: GroupRepresentation = await kc.groups.by_id(group_id).get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return GroupRepresentation.from_dict(response.json())

    async def update(self, group_representation: GroupRepresentation):
        """Update a group by id.

        .. code:: python

            group_representation = GroupRepresentation(name="group-name")
            await kc.groups.by_id(group_id).update(group_representation)
        """
        connection = await self._get_connection()
        await connection.put(self.get_url(), json=group_representation.to_dict())

    async def delete(self):
        """Delete a group by id.

        .. code:: python

            await kc.groups.by_id(group_id).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
