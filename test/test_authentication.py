import pytest
from utils import assert_not_raises

from keycloak_admin_aio import KeycloakAdmin


class TestRequiredActions:
    @pytest.mark.asyncio
    @assert_not_raises
    async def test_get(self, keycloak_admin: KeycloakAdmin):
        await keycloak_admin.authentication.required_actions.get()
