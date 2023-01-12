from .. import AttachedResources, KeycloakResource
from .brute_force import BruteForce


class AttackDetection(KeycloakResource):
    """Provides the Keycloak attack-detection resource."""

    _keycloak_resources: AttachedResources = [("brute_force", BruteForce)]
    brute_force: BruteForce

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/attack-detection"
