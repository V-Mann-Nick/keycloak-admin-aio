import asyncio
from datetime import datetime, timedelta
from typing import Any, Literal, Optional

import httpx

from .lib.utils import remove_none
from .resources import KeycloakResourcesType
from .resources.client_scopes import ClientScopes
from .resources.roles import Roles
from .resources.users import Users
from .resources.clients import Clients
from .resources.admin_events import AdminEvents
from .resources.authentication import Authentication
from .resources.groups import Groups


class KeycloakAdmin:
    __keycloak_resources: KeycloakResourcesType = [
        ("roles", Roles),
        ("client_scopes", ClientScopes),
        ("users", Users),
        ("clients", Clients),
        ("admin_events", AdminEvents),
        ("authentication", Authentication),
        ("groups", Groups),
    ]
    roles: Roles
    client_scopes: ClientScopes
    users: Users
    clients: Clients
    admin_events: AdminEvents
    authentication: Authentication
    groups: Groups

    def __init__(
        self,
        server_url: str,
        grant_type: Literal["client_credentials", "password"],
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        realm: str = "master",
        httpx_args={},
    ):
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

        async def raise_for_status_hook(response: httpx.Response):
            response.raise_for_status()

        self.__connection = httpx.AsyncClient(
            event_hooks={"response": [raise_for_status_hook]}, **httpx_args
        )
        self.__access_token = None
        self.__refresh_token = None
        self.__set_keycloak_resources()

    @classmethod
    def with_client_credentials(
        cls,
        server_url: str,
        client_id: str,
        client_secret: str,
        realm: str = "master",
        httpx_args={},
    ):
        return cls(
            server_url,
            grant_type="client_credentials",
            client_id=client_id,
            client_secret=client_secret,
            realm=realm,
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
        httpx_args={},
    ):
        return cls(
            server_url,
            grant_type="password",
            client_id=client_id,
            username=username,
            password=password,
            realm=realm,
            httpx_args=httpx_args,
        )

    @property
    def realm(self):
        return self._realm

    @property
    def username(self):
        return self._username

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self.client_secret

    @property
    def password(self):
        return self._password

    @property
    def server_url(self):
        return self._server_url

    @property
    def grant_type(self):
        return self._grant_type

    def get_url(self):
        return f"{self._server_url}/admin/realms/{self._realm}"

    async def close(self):
        await self.__connection.aclose()

    def close_sync(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.close())

    def __set_keycloak_resources(self):
        for resources_name, Resource in self.__keycloak_resources:
            setattr(self, resources_name, Resource(self.__get_connection, self.get_url))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_, **__):
        await self.close()

    async def get_access_token(self):
        if not self.__access_token:
            await self.__token()
        else:
            now = datetime.now()
            if now > self.access_token_expire:
                if now < self.refresh_token_expire:
                    await self.__token()
                else:
                    await self.__token_refresh()
        return self.__access_token

    def get_token_url(self) -> str:
        return f"{self._server_url}/realms/{self._realm}/protocol/openid-connect/token"

    def __parse_token_response(self, token_response: dict[str, Any]):
        self.__access_token = token_response["access_token"]
        self.__refresh_token = token_response.get("refresh_token")
        self.access_token_expire = datetime.now() + timedelta(
            seconds=token_response["expires_in"] - 10
        )
        self.refresh_token_expire = datetime.now() + timedelta(
            seconds=token_response.get("refresh_expires_in", 0) - 10
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
        response = await self.__connection.post(
            self.get_token_url(), data=payload, headers=headers
        )
        self.__parse_token_response(response.json())

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
