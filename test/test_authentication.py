from utils import assert_not_raises

from keycloak_admin_aio import KeycloakAdmin


class TestRequiredActions:
    @assert_not_raises
    async def test_get(self, keycloak_admin: KeycloakAdmin):
        await keycloak_admin.authentication.required_actions.get()
