import pytest

from keycloak_admin_aio import KeycloakAdmin


@pytest.fixture
async def keycloak_admin():
    async with KeycloakAdmin.with_password(
        server_url="http://localhost:8080/auth", username="testing", password="testing"
    ) as kc:
        yield kc
