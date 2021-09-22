from ..... import KeycloakResource


class UsersByIdGroupsById(KeycloakResource):
    def get_url(self, user_id: str, group_id: str) -> str:
        return f"{self._get_parent_url(user_id)}/{group_id}"

    async def add(self, user_id: str, group_id: str):
        connection = await self._get_connection()
        await connection.put(self.get_url(user_id, group_id))

    async def delete(self, user_id: str, group_id: str):
        connection = await self._get_connection()
        await connection.delete(self.get_url(user_id, group_id))
