from keycloak_admin_aio.types import GroupRepresentation

from .... import KeycloakResource


class GroupsByIdChildren(KeycloakResource):
    """Get children of a group by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, GroupRepresentation

        kc: KeycloakAdmin  # must be instantiated
        group_id: str  # uuid
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/children"

    async def create(self, group_representation: GroupRepresentation):
        """Create a parent/child group relationship.

        .. code:: python

            group_representation = GroupRepresentation(name="child-group-name")
            await kc.goups.by_id(group_id).children.add(group_representation)
        """
        connection = await self._get_connection()
        await connection.post(self.get_url(), json=group_representation.to_dict())
