from typing import Any

from ..... import KeycloakResourceWithIdentifier


class UsersByIdBruteForceDetection(KeycloakResourceWithIdentifier):
    """Provides the users by id on brute-force detection resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin

        kc: KeycloakAdmin  # needs to be instantiated
        user_id: str  # uuid
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def get(self) -> dict[str, Any]:
        """Get status of a user for brute-force detection.

        .. code:: python

            result: dict[str, Any] = await kc.attack_detection.brute_force.users.by_id(user_id).get()
        """
        connection = await self._get_connection()
        response = await connection.get(self.get_url())
        return response.json()

    async def delete(self):
        """Clear login failures for the user.

        .. code:: python

            await kc.attack_detection.brute_force.users.by_id(user_id).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
