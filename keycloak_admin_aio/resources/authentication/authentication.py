from keycloak_admin_aio.resources.keycloak_resource import KeycloakResourcesType

from .. import KeycloakResource
from .required_actions import AuthenticationRequiredActions


class Authentication(KeycloakResource):
    _keycloak_resources: KeycloakResourcesType = [
        ("required_actions", AuthenticationRequiredActions)
    ]
    required_actions: AuthenticationRequiredActions

    def get_url(self):
        return f"{self._get_parent_url()}/authentication"
