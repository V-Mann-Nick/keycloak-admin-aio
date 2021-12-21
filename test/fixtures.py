import asyncio

import pytest

from keycloak_admin_aio import KeycloakAdmin


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def keycloak_admin():
    async with KeycloakAdmin.with_password(
        server_url="http://localhost:8080/auth", username="testing", password="testing"
    ) as kc:
        yield kc
