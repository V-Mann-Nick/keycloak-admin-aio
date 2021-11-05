from ..... import KeycloakResourceWithIdentifier


class UsersByIdGroupsById(KeycloakResourceWithIdentifier):
    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def create(self):
        connection = await self._get_connection()
        await connection.put(self.get_url())

    async def delete(self):
        connection = await self._get_connection()
        await connection.delete(self.get_url())
