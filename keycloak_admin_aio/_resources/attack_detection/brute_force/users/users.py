from .... import (
    AttachedResources,
    KeycloakResource,
    KeycloakResourceWithIdentifierGetter,
)
from .by_id import UsersByIdBruteForceDetection


class Users(KeycloakResource):
    """Provides the users on brute-force detection resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin

        kc: KeycloakAdmin  # needs to be instantiated
    """

    _keycloak_resources: AttachedResources = [("by_id", UsersByIdBruteForceDetection)]
    by_id: KeycloakResourceWithIdentifierGetter[UsersByIdBruteForceDetection]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/users"

    async def delete(self):
        """Clear login failures for all users.

        .. code:: python

            await kc.attack_detection.brute_force.users.delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
