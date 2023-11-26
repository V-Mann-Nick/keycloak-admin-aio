import asyncio
import os
import subprocess
from typing import Literal

import httpx
import pytest
from dependencies import sort_items

from keycloak_admin_aio import KeycloakAdmin

KEYCLOAK_VERSION = os.environ.get("KEYCLOAK_VERSION", "latest")
KEYCLOAK_IMAGE = f"quay.io/keycloak/keycloak:{KEYCLOAK_VERSION}"
CONTAINER_NAME = "keycloak_testing_target"
KEYCLOAK_ADMIN = "testing"
KEYCLOAK_PASSWORD = "testing"
KEYCLOAK_HOST = "127.0.0.1"
KEYCLOAK_PORT = 8080
KEYCLOAK_URL = f"http://{KEYCLOAK_HOST}:{KEYCLOAK_PORT}"


def check_container_command_exists(command: Literal["docker", "podman"]):
    """Check if a container command exists."""
    try:
        subprocess.run([command, "info"], stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


def determine_container_runtime():
    """Check if Docker or Podman is installed."""
    if check_container_command_exists("docker"):
        return "docker"
    elif check_container_command_exists("podman"):
        return "podman"
    else:
        raise RuntimeError("Neither Docker nor Podman are installed.")


async def wait_for_server_to_start():
    """Wait for Keycloak server to start."""
    async with httpx.AsyncClient() as client:
        for _ in range(60):
            try:
                response = await client.get(f"{KEYCLOAK_URL}/health/ready")
                response.raise_for_status()
                if response.status_code == 200:
                    # Not sure why but we still have to wait a bit more in CI
                    # otherwise Keycloak will sometimes return 401 for token
                    await asyncio.sleep(1)
                    return
            except httpx.HTTPError:
                ...
            await asyncio.sleep(1)


@pytest.fixture(scope="session", autouse=True)
async def run_keycloak(request: pytest.FixtureRequest):
    """Run Keycloak in a container."""
    container_runtime = determine_container_runtime()
    subprocess.run(
        [
            container_runtime,
            "run",
            "-d",
            "--rm",
            "--env",
            f"KEYCLOAK_ADMIN={KEYCLOAK_ADMIN}",
            "--env",
            f"KEYCLOAK_ADMIN_PASSWORD={KEYCLOAK_PASSWORD}",
            "--env",
            "KC_HEALTH_ENABLED=true",
            "-p",
            f"{KEYCLOAK_PORT}:8080",
            "--name",
            CONTAINER_NAME,
            KEYCLOAK_IMAGE,
            "start-dev",
        ]
    )
    request.addfinalizer(
        lambda: subprocess.run([container_runtime, "rm", "-f", CONTAINER_NAME])
    )
    await wait_for_server_to_start()
    return


def pytest_report_header():
    return f"Keycloak version: {KEYCLOAK_VERSION}"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session scope.

    See: https://pytest-asyncio.readthedocs.io/en/latest/reference/decorators.html
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def keycloak_admin():
    """Instantiate the KeycloakAdmin client."""
    async with KeycloakAdmin.with_password(
        server_url=KEYCLOAK_URL, username=KEYCLOAK_ADMIN, password=KEYCLOAK_PASSWORD
    ) as kc:
        yield kc


def pytest_collection_modifyitems(
    session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
):
    sort_items(items)
