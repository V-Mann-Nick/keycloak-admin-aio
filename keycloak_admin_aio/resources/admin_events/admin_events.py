from typing import Optional

from keycloak_admin_aio.lib.utils import remove_none
from keycloak_admin_aio.types import OperationType, ResourceType

from .. import KeycloakResource


class AdminEvents(KeycloakResource):
    def get_url(self):
        return f"{self._get_parent_url()}/admin-events"

    async def get(
        self,
        auth_client: Optional[str] = None,
        auth_ip_address: Optional[str] = None,
        auth_realm: Optional[str] = None,
        auth_user: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        first: Optional[int] = None,
        max: Optional[int] = None,
        operation_types: Optional[list[OperationType]] = None,
        resource_path: Optional[str] = None,
        resource_types: Optional[list[ResourceType]] = None,
    ) -> list[dict]:
        connection = await self._get_connection()
        params = remove_none(
            {
                "authClient": auth_client,
                "authIpAddress": auth_ip_address,
                "authRealm": auth_realm,
                "authUser": auth_user,
                "dateFrom": date_from,
                "dateTo": date_to,
                "first": first,
                "max": max,
                "operationTypes": operation_types,
                "resourcePath": resource_path,
                "resourceTypes": resource_types,
            }
        )
        response = await connection.get(self.get_url(), params=params)
        return response.json()
