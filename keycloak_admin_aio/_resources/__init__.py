"""This package provides classes for Keycloak resources."""

from .keycloak_resource import (
    KeycloakResource,
    KeycloakResourcesType,
    KeycloakResourceWithIdentifier,
    KeycloakResourceWithIdentifierGetter,
)

from .admin_events import AdminEvents
from .authentication import Authentication
from .client_scopes import ClientScopes
from .clients import Clients
from .groups import Groups
from .roles import Roles
from .users import Users
