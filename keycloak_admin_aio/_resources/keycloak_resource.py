from __future__ import annotations

import abc
from typing import Any, Awaitable, Callable, Generic, TypeVar

import httpx

GetConnectionFn = Callable[..., Awaitable[httpx.AsyncClient]]
GetUrlFn = Callable[..., str]


def _create_getter(
    resource: Any,
    get_connection: GetConnectionFn,
    get_url: GetUrlFn,
):
    """Creates a getter function for identified resources.

    This function creator helper is required as using a lambda as an inline
    function leads to a reference problem with Python.
    """
    return lambda identifier: resource(get_connection, get_url, identifier)


class KeycloakResource:
    """Base class for all Keycloak resources.

    It attaches all the child resources in ``_keycloak_resources``
    """

    _keycloak_resources: AttachedResources

    def __init__(
        self,
        get_connection: GetConnectionFn,
        get_parent_url: GetUrlFn,
    ):
        """Initialize keycloak resource."""
        self._get_connection = get_connection
        self._get_parent_url = get_parent_url
        self.__set_keycloak_resources()

    @abc.abstractmethod
    def get_url(self) -> str:
        """Get the resource's url."""

    def __set_keycloak_resources(self):
        """Attaches all the specified child resources to the class instance.

        On init this method will parse the list of ``_keycloak_resources``
        attaching a getter for identified resources and a class instance for
        others.
        """
        if not hasattr(self, "_keycloak_resources"):
            return
        for resources_name, resource in self._keycloak_resources:
            if issubclass(resource, KeycloakResourceWithIdentifier):
                setattr(
                    self,
                    resources_name,
                    _create_getter(resource, self._get_connection, self.get_url),
                )
            else:
                setattr(
                    self, resources_name, resource(self._get_connection, self.get_url)
                )


class KeycloakResourceWithIdentifier(KeycloakResource):
    """Base class for all identified keycloak resources.

    These class instances will be provided via getters.
    E.g. ``kc.roles.by_name("some-role").get()``
    """

    def __init__(
        self,
        get_connection: GetConnectionFn,
        get_parent_url: GetUrlFn,
        identifier: str,
    ):
        """Initializes an identified keycloak resources adding the identifier."""
        super().__init__(get_connection, get_parent_url)
        self.identifier = identifier


AttachedResources = list[tuple[str, type[KeycloakResource]]]

T = TypeVar("T", bound=KeycloakResourceWithIdentifier)


class KeycloakResourceWithIdentifierGetter(Generic[T]):
    """Function which attaches to Keycloak resources to provide a child resource by identifier.

    Using ``Callable`` does not properly work and although (as far as I
    understand) it should be fixed: https://github.com/python/mypy/issues/708.
    Honestly I really don't understand what's going on here, but writing it
    this way resolved the mypy issue I was having
    """

    def __call__(self, identifier: str) -> T:
        ...
