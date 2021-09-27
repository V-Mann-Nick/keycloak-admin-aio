import abc
from typing import Any, Callable, Coroutine, TypeVar

from httpx import AsyncClient


def create_getter(
    Resource: Any,
    get_connection: Callable[..., Coroutine[Any, Any, AsyncClient]],
    get_url: Callable[..., str],
):
    """
        Creates a getter function for identified resources.  This function
        creator helper is required as using a lambda as an inline function leads to
        a reference problem with Python.
    """
    return lambda identifier: Resource(get_connection, get_url, identifier)


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
    def get_url(self) -> str:
        ...

    def __set_keycloak_resources(self):
        if not hasattr(self, "_keycloak_resources"):
            return
        for resources_name, Resource in self._keycloak_resources:
            if issubclass(Resource, KeycloakResourceWithIdentifier):
                setattr(
                    self,
                    resources_name,
                    create_getter(Resource, self._get_connection, self.get_url),
                )
            else:
                setattr(
                    self, resources_name, Resource(self._get_connection, self.get_url)
                )


class KeycloakResourceWithIdentifier(KeycloakResource):
    def __init__(
        self,
        get_connection: Callable[..., Coroutine[Any, Any, AsyncClient]],
        get_parent_url: Callable[..., str],
        identifier: str,
    ):
        super().__init__(get_connection, get_parent_url)
        self.identifier = identifier


KeycloakResourcesType = list[tuple[str, type[KeycloakResource]]]

T = TypeVar("T", bound=KeycloakResourceWithIdentifier)
KeycloakResourceWithIdentifierGetter = Callable[[str], T]
