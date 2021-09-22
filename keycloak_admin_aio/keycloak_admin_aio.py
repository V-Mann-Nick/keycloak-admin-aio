import asyncio
from datetime import datetime, timedelta
import logging
from typing import Literal, Optional

import httpx

from .resources import KeycloakResourcesType
from .resources.roles import Roles
from .resources.client_scopes import ClientScopes
from .resources.users import Users

URL_TOKEN = "realms/{realm-name}/protocol/openid-connect/token"


class KeycloakAdmin:
    __keycloak_resources: KeycloakResourcesType = [
        ("roles", Roles),
        ("client_scopes", ClientScopes),
        ("users", Users),
    ]
    roles: Roles
    client_scopes: ClientScopes
    users: Users

    def __init__(
        self,
        server_url: str,
        grant_type: Literal["client_credentials", "password"],
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        realm: str = "master",
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
            event_hooks={"response": [raise_for_status_hook]}
        )
        self.__access_token = None
        self.__refresh_token = None
        self.__set_keycloak_resources()

    @classmethod
    def with_client_credentials(
        cls, server_url: str, client_id: str, client_secret: str, realm: str = "master"
    ):
        return cls(
            server_url,
            grant_type="client_credentials",
            client_id=client_id,
            client_secret=client_secret,
            realm=realm,
        )

    @classmethod
    def with_password(
        cls,
        server_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = "admin-cli",
        realm: str = "master",
    ):
        return cls(
            server_url,
            grant_type="password",
            client_id=client_id,
            username=username,
            password=password,
            realm=realm,
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

    async def get_access_token(self):
        if not self.__access_token or not self.__refresh_token:
            await self.__token("access_token")
        else:
            now = datetime.now()
            if now > self.access_token_expire:
                if now < self.refresh_token_expire:
                    await self.__token("refresh_token")
                else:
                    await self.__token("access_token")
        return self.__access_token

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

    async def __token(
        self,
        token_type: Literal["access_token", "refresh_token"],
    ):
        token_endpoint = f"{self._server_url}/{URL_TOKEN}".format(
            **{"realm-name": self._realm}
        )
        headers = httpx.Headers({"Content-Type": "application/x-www-form-urlencoded"})
        payload = {"client_id": self._client_id}
        if token_type == "refresh_token":
            payload.update(
                {
                    "grant_type": "refresh_token",
                    "refresh_token": self.__refresh_token,
                }
            )
        elif token_type == "access_token":
            grant_type = self.grant_type
            payload.update(
                {
                    "grant_type": grant_type,
                }
            )
            if grant_type == "client_credentials":
                payload.update(
                    {"client_id": self._client_id, "client_secret": self._client_secret}
                )
            else:
                payload.update({"username": self._username, "password": self._password})
        else:
            raise Exception(
                "Positional argument 'token_type' needs to be either 'access_token' or 'refresh_token'"
            )
        logging.debug(f"token payload: {payload}")
        response = await self.__connection.post(
            token_endpoint, data=payload, headers=headers
        )
        token = response.json()
        self.__access_token = token["access_token"]
        self.__refresh_token = token.get("refresh_token")
        self.access_token_expire = datetime.now() + timedelta(
            seconds=token["expires_in"] - 10
        )
        self.refresh_token_expire = datetime.now() + timedelta(
            seconds=token.get("refresh_expires_in", 0) - 10
        )

    async def __get_connection(self):
        access_token = await self.get_access_token()

        def auth_interceptor(request: httpx.Request) -> httpx.Request:
            request.headers["Authorization"] = f"Bearer {access_token}"
            return request

        self.__connection.auth = auth_interceptor
        return self.__connection
