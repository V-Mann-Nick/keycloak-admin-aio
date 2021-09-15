import abc
from typing import Any, Callable, Coroutine

from httpx import AsyncClient


class KeycloakResource:
    def __init__(
        self,
        get_connection: Callable[..., Coroutine[Any, Any, AsyncClient]],
        get_parent_url: Callable[..., str],
    ):
        self._get_connection = get_connection
        self._get_parent_url = get_parent_url
        self.__set_keycloak_resources()

    @abc.abstractmethod
    def get_url(self):
        ...

    def __set_keycloak_resources(self):
        if not hasattr(self, "_keycloak_resources"):
            return
        for resources_name, Resource in self._keycloak_resources:
            setattr(self, resources_name, Resource(self._get_connection, self.get_url))


KeycloakResourcesType = list[tuple[str, type[KeycloakResource]]]
