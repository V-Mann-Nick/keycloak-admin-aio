from ... import AttachedResources, KeycloakResource
from .users import Users


class BruteForce(KeycloakResource):
    """Provides the Keycloak brute-force resource."""

    _keycloak_resources: AttachedResources = [("users", Users)]
    users: Users

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/brute-force"
