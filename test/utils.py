import functools
import warnings
from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Awaitable, Callable, Generic, Literal, Optional, TypeVar, Union

import httpx
import pytest
import pytest_asyncio
from pytest_dependency import depends

TFunction = TypeVar("TFunction", bound=Callable[..., Awaitable])


def assert_not_raises(message: str) -> Callable[[TFunction], TFunction]:
    """Decorator to assert that a test does not raise a HTTPError exception."""

    def inner(func: TFunction) -> TFunction:
        @functools.wraps(func)
        async def new_func(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except httpx.HTTPError as e:
                assert False, f"{message}: {e}"

        return new_func  # type: ignore

    return inner


def assert_not_raises_with_class_name(
    message: Callable[[str], str]
) -> Callable[[TFunction], TFunction]:
    """Sames as `assert_not_raises` but it extracts the class_name when inherited."""

    def inner(func: TFunction) -> TFunction:
        @functools.wraps(func)
        async def new_func(self, *args, **kwargs):
            return await assert_not_raises(message(self.__class__.__name__))(func)(
                self, *args, **kwargs
            )

        return new_func  # type: ignore

    return inner


LifeCycleTestType = Literal["create", "get", "update", "delete"]


TResourceRepresentation = TypeVar("TResourceRepresentation")


ResourceCreate = Callable[[], Awaitable[Optional[str]]]
ResourceGet = Callable[[Optional[str]], Awaitable[TResourceRepresentation]]
ResourceUpdate = Optional[Callable[[Optional[str]], Awaitable[None]]]
ResourceDelete = Callable[[Optional[str]], Awaitable[None]]


class Value:
    """Helper class to store a value in a pytest fixture."""

    value: Optional[str] = None

    def get(self):
        return self.value

    def set(self, value: Union[str, None]):
        self.value = value


DependencyScope = Literal["session", "module", "class"]
ExtraDependency = Union[str, tuple[str, DependencyScope]]


class ResourceLifeCycleTest(ABC, Generic[TResourceRepresentation]):
    """Base class for testing the lifecycle of a keycloak resource."""

    """Extra dependencies to add to each test."""
    EXTRA_DEPENDENCIES: list[ExtraDependency] = []

    """Extra dependencies to add to the create test."""
    EXTRA_DEPENDENCIES_CREATE: list[ExtraDependency] = []

    """Extra dependencies to add to the get test."""
    EXTRA_DEPENDENCIES_GET: list[ExtraDependency] = []

    """Extra dependencies to add to the update test."""
    EXTRA_DEPENDENCIES_UPDATE: list[ExtraDependency] = []

    """Extra dependencies to add to the delete test."""
    EXTRA_DEPENDENCIES_DELETE: list[ExtraDependency] = []

    def check_dependencies(
        self, request: pytest.FixtureRequest, test_type: LifeCycleTestType
    ):
        extra_dependencies_by_type = {
            "create": self.EXTRA_DEPENDENCIES_CREATE,
            "get": self.EXTRA_DEPENDENCIES_GET,
            "update": self.EXTRA_DEPENDENCIES_UPDATE,
            "delete": self.EXTRA_DEPENDENCIES_DELETE,
        }
        dependencies = [
            *self.EXTRA_DEPENDENCIES,
            *extra_dependencies_by_type[test_type],
        ]
        for dependency in dependencies:
            if isinstance(dependency, str):
                depends(request, [dependency], scope="module")
            else:
                name, scope = dependency
                depends(request, [name], scope=scope)

    @classmethod
    def dependency_name(
        cls, test_type: LifeCycleTestType, scope: DependencyScope = "module"
    ) -> str:
        """Returns the dependency name for the given test type and scope."""
        test_name = f"test_{test_type}"
        name_by_scope = {
            "session": f"test/{cls.__module__}.py::{cls.__name__}::{test_name}",
            "module": f"{cls.__name__}::{test_name}",
            "class": test_name,
        }
        return name_by_scope[scope]

    @abstractmethod
    @pytest.fixture(scope="class")
    def create(self) -> ResourceCreate:
        """Returns a function that creates a resource and returns its identifier."""

    @abstractmethod
    @pytest.fixture(scope="class")
    def get(self) -> ResourceGet:
        """Returns a function that gets a resource."""

    @abstractmethod
    @pytest.fixture(scope="class")
    def update(self) -> Optional[ResourceUpdate]:
        """Returns a function that updates a resource. May return None if not applicable."""

    @abstractmethod
    @pytest.fixture(scope="class")
    def delete(self) -> ResourceDelete:
        """Returns a function that deletes a resource."""

    @pytest_asyncio.fixture(scope="class")
    async def identifier(self, delete: ResourceDelete):
        """Fixture to store the identifier of the resource accross the lifecycle.

        It attempts cleanup of the resource after the tests are done.
        If the resource was already deleted, we don't want to raise an error.
        If the resource can't be deleted due to a buggy delete function, a
        warning is emmited and the exception is re-raised as this could cascade
        to other tests.
        """
        identifier = Value()
        yield identifier
        id = identifier.get()
        if not id:
            return
        try:
            await delete(id)
        except Exception as ex:
            if isinstance(ex, httpx.HTTPStatusError) and ex.response.status_code == 404:
                return
            warnings.warn(
                dedent(
                    f"""Could not cleanup resource with id '{id}' in {self.__class__.__name__}.
                    This could cause issues with other tests."""
                ).replace("\n", " ")
            )
            raise ex

    @pytest.mark.asyncio
    @pytest.mark.dependency()
    @assert_not_raises_with_class_name(
        lambda class_name: f"Could not create in {class_name}"
    )
    async def test_create(
        self, create: ResourceCreate, identifier: Value, request: pytest.FixtureRequest
    ):
        """Test the create method."""
        self.check_dependencies(request, "create")
        identifier.set(await create())

    @pytest.mark.asyncio
    @pytest.mark.dependency()
    @assert_not_raises_with_class_name(
        lambda class_name: f"Could not get in {class_name}"
    )
    async def test_get(
        self, get: ResourceGet, identifier: Value, request: pytest.FixtureRequest
    ):
        """Test the get method."""
        self.check_dependencies(request, "get")
        depends(request, ["test_create"], scope="class")
        await get(identifier.get())

    @pytest.mark.asyncio
    @pytest.mark.dependency()
    @assert_not_raises_with_class_name(
        lambda class_name: f"Could not update in {class_name}"
    )
    async def test_update(
        self,
        update: Optional[ResourceUpdate],
        identifier: Value,
        request: pytest.FixtureRequest,
    ):
        """Test the update method."""
        self.check_dependencies(request, "update")
        depends(request, ["test_get"], scope="class")
        if not update:
            pytest.skip(f"Update not implemented in {self.__class__.__name__}")
        await update(identifier.get())

    @pytest.mark.asyncio
    @pytest.mark.dependency()
    @assert_not_raises_with_class_name(
        lambda class_name: f"Could not delete in {class_name}"
    )
    async def test_delete(
        self,
        delete: ResourceDelete,
        update: Optional[ResourceUpdate],
        identifier: Value,
        request: pytest.FixtureRequest,
    ):
        """Test the delete method."""
        self.check_dependencies(request, "delete")
        if update:
            depends(request, ["test_update"], scope="class")
        else:
            depends(request, ["test_get"], scope="class")
        await delete(identifier.get())
