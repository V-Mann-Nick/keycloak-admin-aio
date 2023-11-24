from utils import assert_not_raises

from keycloak_admin_aio import KeycloakAdmin


@assert_not_raises
async def test_get(keycloak_admin: KeycloakAdmin):
    await keycloak_admin.admin_events.get()
