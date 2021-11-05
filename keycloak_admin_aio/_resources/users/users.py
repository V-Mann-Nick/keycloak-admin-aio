from typing import Optional

from keycloak_admin_aio._lib.utils import (
    get_resource_id_in_location_header,
    remove_none,
)
from keycloak_admin_aio.types import UserRepresentation

from .. import AttachedResources, KeycloakResource, KeycloakResourceWithIdentifierGetter
from .by_id import UsersById


class Users(KeycloakResource):
    """Provides the Keycloak user resource.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin, UserRepresentation

        kc: KeycloakAdmin  # needs to be instantiated
    """

    _keycloak_resources: AttachedResources = [("by_id", UsersById)]
    by_id: KeycloakResourceWithIdentifierGetter[UsersById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/users"

    async def get(
        self,
        brief_representation: Optional[bool] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
        search: Optional[str] = None,
        email: Optional[str] = None,
        email_verified: Optional[bool] = None,
        enabled: Optional[bool] = None,
        exact: Optional[bool] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        idp_alias: Optional[str] = None,
        idp_user_id: Optional[str] = None,
        username: Optional[str] = None,
    ) -> list[UserRepresentation]:
        """Get users.

        .. code:: python

            users: list[UserRepresentation] = await kc.users.get()
        """
        connection = await self._get_connection()
        params = remove_none(
            {
                "briefRepresentation": brief_representation,
                "first": first,
                "max": max,
                "search": search,
                "email": email,
                "emailVerified": email_verified,
                "enabled": enabled,
                "exact": exact,
                "firstName": first_name,
                "lastName": last_name,
                "idpAlias": idp_alias,
                "ipdUserId": idp_user_id,
                "username": username,
            }
        )
        response = await connection.get(self.get_url(), params=params)
        return UserRepresentation.from_list(response.json())

    async def create(self, user_representation: UserRepresentation) -> str:
        """Create user.

        .. code:: python

            user_representation = UserRepresentation(email="user@domain.com")
            user_id: str = await kc.users.create(user_representation)
        """
        connection = await self._get_connection()
        response = await connection.post(
            self.get_url(), json=user_representation.to_dict()
        )
        return get_resource_id_in_location_header(response)

    async def count(
        self,
        search: Optional[str] = None,
        email: Optional[str] = None,
        email_verified: Optional[bool] = None,
        exact: Optional[bool] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
    ) -> int:
        """User count.

        .. code:: python

            user_count: int = await kc.users.count()
        """
        connection = await self._get_connection()
        params = remove_none(
            {
                "search": search,
                "email": email,
                "emailVerified": email_verified,
                "exact": exact,
                "firstName": first_name,
                "lastName": last_name,
                "username": username,
            }
        )
        response = await connection.get(f"{self.get_url()}/count", params=params)
        return int(response.text)
