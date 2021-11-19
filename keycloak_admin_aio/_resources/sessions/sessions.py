from .. import AttachedResources, KeycloakResource, KeycloakResourceWithIdentifierGetter
from .by_id import SessionsById


class Sessions(KeycloakResource):
    """Provides realm sessions."""

    _keycloak_resources: AttachedResources = [("by_id", SessionsById)]
    by_id: KeycloakResourceWithIdentifierGetter[SessionsById]

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/sessions"
