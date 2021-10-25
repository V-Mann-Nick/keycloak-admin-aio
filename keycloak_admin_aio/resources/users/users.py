from typing import Optional

from keycloak_admin_aio.lib.utils import get_resource_id_in_location_header, remove_none
from keycloak_admin_aio.resources.keycloak_resource import KeycloakResourcesType
from keycloak_admin_aio.types import UserRepresentation

from .. import KeycloakResource, KeycloakResourceWithIdentifierGetter
from .by_id import UsersById


class Users(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [("by_id", UsersById)]
    by_id: KeycloakResourceWithIdentifierGetter[UsersById]

    def get_url(self):
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
