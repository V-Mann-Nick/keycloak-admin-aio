"""This package provides a asynchronous Keycloak Admin API wrapper."""

from ._keycloak_admin_aio import KeycloakAdmin
from .types import *

__all__ = ["KeycloakAdmin"]
