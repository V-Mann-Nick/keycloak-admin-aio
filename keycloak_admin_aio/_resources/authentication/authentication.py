from .. import KeycloakResource, KeycloakResourcesType
from .required_actions import AuthenticationRequiredActions


class Authentication(KeycloakResource):
    """Provides the Keycloak authentication management resource."""

    _keycloak_resources: KeycloakResourcesType = [
        ("required_actions", AuthenticationRequiredActions)
    ]
    required_actions: AuthenticationRequiredActions

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/authentication"
