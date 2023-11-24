import pytest
import test_users
from utils import assert_not_raises

from keycloak_admin_aio import KeycloakAdmin, UserRepresentation


class TestBruteForce:
    DEPENDENCIES = [
        test_users.TestByIdLifeCycle.dependency_name("create", scope="session"),
        test_users.TestByIdLifeCycle.dependency_name("delete", scope="session"),
    ]

    @pytest.fixture(scope="class")
    async def user_id(self, keycloak_admin: KeycloakAdmin):
        user_id = await keycloak_admin.users.create(
            UserRepresentation(email="test@test.com", username="test")
        )
        yield user_id
        await keycloak_admin.users.by_id(user_id).delete()

    @pytest.mark.dependency(depends=DEPENDENCIES, scope="session")
    @assert_not_raises
    async def test_get(self, keycloak_admin: KeycloakAdmin, user_id: str):
        status = await keycloak_admin.attack_detection.brute_force.users.by_id(
            user_id
        ).get()
        assert status is not None
        assert type(status) is dict

    @pytest.mark.dependency(depends=DEPENDENCIES, scope="session")
    @assert_not_raises
    async def test_delete_all(self, keycloak_admin: KeycloakAdmin):
        await keycloak_admin.attack_detection.brute_force.users.delete()

    @pytest.mark.dependency(depends=DEPENDENCIES, scope="session")
    @assert_not_raises
    async def test_delete_by_id(self, keycloak_admin: KeycloakAdmin, user_id: str):
        await keycloak_admin.attack_detection.brute_force.users.by_id(user_id).delete()
