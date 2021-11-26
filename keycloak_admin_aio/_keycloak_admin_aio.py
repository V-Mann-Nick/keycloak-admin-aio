from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Any, Literal, Optional

import httpx

from ._httpx_args import merge_with_default_httpx_args
from ._lib.utils import remove_none
from ._resources import (
    AdminEvents,
    AttachedResources,
    Authentication,
    Clients,
    ClientScopes,
    Groups,
    Roles,
    Sessions,
    Users,
)


class KeycloakAdmin:
    """Base class for Keycloak Admin API endpoints.

    It handles the ``access_token`` and guarantees it being valid when using the
    ``get_access_token`` method or accessing a protected Keycloak resource.
    """

    __keycloak_resources: AttachedResources = [
        ("roles", Roles),
        ("client_scopes", ClientScopes),
        ("users", Users),
        ("clients", Clients),
        ("admin_events", AdminEvents),
        ("authentication", Authentication),
        ("groups", Groups),
        ("sessions", Sessions),
    ]
    roles: Roles
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_roles_resource"""

    client_scopes: ClientScopes
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_client_scopes_resource"""

    users: Users
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_users_resource"""

    clients: Clients
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_clients_resource"""

    admin_events: AdminEvents
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_realms_admin_resource"""

    authentication: Authentication
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_authentication_management_resource"""

    groups: Groups
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_groups_resource"""

    sessions: Sessions

    leeway: int
    """A token will be considered as expired seconds before its actual expiry controlled by this value."""

    def __init__(
        self,
        server_url: str,
        grant_type: Literal["client_credentials", "password"],
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        realm: str = "master",
        leeway: int = 10,
        httpx_args={},
    ):
        """Initialize ``KeycloakAdmin`` with either client or user credentials.

        Should not be used directly. The usage
        of ``with_client_credentials`` or ``with_password`` should be
        preferred.
        """
        allowed_grant_types = ["client_credentials", "password"]
        if not any([grant_type == allowed for allowed in allowed_grant_types]):
            raise Exception(f"'grant_type' needs to be in '{allowed_grant_types}'")
        self._realm = realm
        self._username = username
        self._client_id = client_id
        self._client_secret = client_secret
        self._password = password
        self._server_url = server_url
        self._grant_type = grant_type
        self.leeway = leeway
        self.__connection = httpx.AsyncClient(
            **merge_with_default_httpx_args(httpx_args)
        )
        self.__access_token = None
        self.__refresh_token = None
        self.__set_keycloak_resources()
        self.__lock = asyncio.Lock()

    @classmethod
    def with_client_credentials(
        cls,
        server_url: str,
        client_id: str,
        client_secret: str,
        realm: str = "master",
        leeway: int = 10,
        httpx_args={},
    ) -> KeycloakAdmin:
        """Instantiate ``KeycloakAdmin`` with ``client_id`` and ``client_secret``."""
        return cls(
            server_url,
            grant_type="client_credentials",
            client_id=client_id,
            client_secret=client_secret,
            realm=realm,
            leeway=leeway,
            httpx_args=httpx_args,
        )

    @classmethod
    def with_password(
        cls,
        server_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = "admin-cli",
        realm: str = "master",
        leeway: int = 10,
        httpx_args={},
    ) -> KeycloakAdmin:
        """Instantiate ``KeycloakAdmin`` with user credentials (username and password)."""
        return cls(
            server_url,
            grant_type="password",
            client_id=client_id,
            username=username,
            password=password,
            realm=realm,
            leeway=leeway,
            httpx_args=httpx_args,
        )

    @property
    def realm(self):
        """Realm property."""
        return self._realm

    @property
    def username(self):
        """Username property."""
        return self._username

    @property
    def client_id(self):
        """Client id property."""
        return self._client_id

    @property
    def client_secret(self):
        """Client secret property."""
        return self.client_secret

    @property
    def password(self):
        """Password property."""
        return self._password

    @property
    def server_url(self):
        """Server url property."""
        return self._server_url

    @property
    def grant_type(self):
        """Token endpoint grant type."""
        return self._grant_type

    def get_url(self):
        """Get the admin api base url."""
        return f"{self._server_url}/admin/realms/{self._realm}"

    async def close(self):
        """Closes open httpx connection."""
        await self.__connection.aclose()

    def close_sync(self):
        """Synchronously close open httpx connection."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.close())

    def __set_keycloak_resources(self):
        for resources_name, resource in self.__keycloak_resources:
            setattr(
                self,
                resources_name,
                resource(self.__get_connection, self.get_url),
            )

    async def __aenter__(self) -> KeycloakAdmin:
        """For entering asynchronous context manger."""
        return self

    async def __aexit__(self, *_, **__):
        """Cleanup for asynchronous context manger."""
        await self.close()

    async def get_access_token(self):
        """Get ``access_token``. Guaranteed not to be expired."""
        async with self.__lock:
            if not self.__access_token:
                await self.__token()
            else:
                now = datetime.now()
                if now > self.access_token_expire:
                    if now < self.refresh_token_expire:
                        await self.__token_refresh()
                    else:
                        await self.__token()
            return self.__access_token

    def get_token_url(self) -> str:
        """Openid connect token endpoint url."""
        return f"{self._server_url}/realms/{self._realm}/protocol/openid-connect/token"

    def __parse_token_response(self, token_response: dict[str, Any]):
        self.__access_token = token_response["access_token"]
        self.__refresh_token = token_response.get("refresh_token")
        self.access_token_expire = datetime.now() + timedelta(
            seconds=token_response["expires_in"] - self.leeway
        )
        self.refresh_token_expire = datetime.now() + timedelta(
            seconds=token_response.get("refresh_expires_in", 0) - self.leeway
        )

    async def __token_refresh(self):
        headers = httpx.Headers({"Content-Type": "application/x-www-form-urlencoded"})
        payload = remove_none(
            {
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.__refresh_token,
            }
        )
        try:
            response = await self.__connection.post(
                self.get_token_url(), data=payload, headers=headers
            )
            self.__parse_token_response(response.json())
        except httpx.HTTPStatusError as ex:
            except_errors = [
                "Refresh token expired",
                "Token is not active",
                "Session not active",
            ]
            error_description = ex.response.json().get("error_description", "")
            if ex.response.status_code == 400 and any(
                error in error_description for error in except_errors
            ):
                await self.__token()

    async def __token(self):
        headers = httpx.Headers({"Content-Type": "application/x-www-form-urlencoded"})
        payload = remove_none(
            {
                "client_id": self._client_id,
                "grant_type": self._grant_type,
                "client_secret": self._client_secret,
                "username": self._username,
                "password": self._password,
            }
        )
        response = await self.__connection.post(
            self.get_token_url(), data=payload, headers=headers
        )
        self.__parse_token_response(response.json())

    async def __get_connection(self):
        access_token = await self.get_access_token()

        def auth_interceptor(request: httpx.Request) -> httpx.Request:
            request.headers["Authorization"] = f"Bearer {access_token}"
            return request

        self.__connection.auth = auth_interceptor
        return self.__connection
