import asyncio
from datetime import datetime, timedelta
from typing import Literal

import httpx

from .resources import KeycloakResourcesType
from .resources.roles import Roles

URL_TOKEN = "realms/{realm-name}/protocol/openid-connect/token"


class KeycloakAdmin:
    __keycloak_resources: KeycloakResourcesType = [("roles", Roles)]

    def __init__(
        self, server_url: str, username: str, password: str, realm: str = "master"
    ):
        self._realm = realm
        self._username = username

        async def raise_for_status_hook(response: httpx.Response):
            response.raise_for_status()

        self.__connection = httpx.AsyncClient(
            event_hooks={"response": [raise_for_status_hook]}
        )
        self.__server_url = server_url
        self.__password = password
        self.__access_token = None
        self.__refresh_token = None
        self.__set_keycloak_resources()

    @property
    def realm(self):
        return self._realm

    @realm.setter
    def realm(self, new_realm):
        self.close_sync()
        self.__init__(self.__server_url, self._username, self.__password, new_realm)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_username):
        self.close_sync()
        self.__init__(self.__server_url, new_username, self.__password, self._realm)

    def get_url(self):
        return f"{self.__server_url}/admin/realms/{self._realm}"

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
        url = f"{self.__server_url}/{URL_TOKEN}".format(**{"realm-name": self._realm})
        headers = httpx.Headers({"Content-Type": "application/x-www-form-urlencoded"})
        if token_type == "refresh_token":
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": self.__refresh_token,
            }
        elif token_type == "access_token":
            payload = {
                "grant_type": "password",
                "username": self._username,
                "password": self.__password,
            }
        else:
            raise Exception(
                "Positional argument 'token_type' needs to be either 'access_token' or 'refresh_token'"
            )
        payload["client_id"] = "admin-cli"
        response = await self.__connection.post(url, data=payload, headers=headers)
        token = response.json()
        self.__access_token = token["access_token"]
        self.__refresh_token = token["refresh_token"]
        self.access_token_expire = datetime.now() + timedelta(
            seconds=token["expires_in"] - 10
        )
        self.refresh_token_expire = datetime.now() + timedelta(
            seconds=token["refresh_expires_in"] - 10
        )

    async def __get_connection(self):
        access_token = await self.get_access_token()

        def auth_interceptor(request: httpx.Request) -> httpx.Request:
            request.headers["Authorization"] = f"Bearer {access_token}"
            return request

        self.__connection.auth = auth_interceptor
        return self.__connection
