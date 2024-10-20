import functools
import warnings
from abc import ABC, abstractmethod
from textwrap import dedent
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Literal,
    Optional,
    TypeVar,
    Union,
    cast,
)

import httpx
import pytest
from dependencies_plugin import Scope, depends

TFunction = TypeVar("TFunction", bound=Callable[..., Awaitable])


def assert_not_raises(func: TFunction) -> TFunction:
    """Decorator to assert that a test does not raise a HTTPError exception."""

    def get_module_name(args: tuple[Any, ...]):
        maybe_self = args[0] if len(args) else None
        if hasattr(maybe_self, "__class__") and hasattr(
            maybe_self.__class__, "__module__"
        ):
            return maybe_self.__class__.__module__
        return func.__module__

    @functools.wraps(func)
    async def new_func(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPError as e:
            assert False, f"{get_module_name(args)}::{func.__name__} unexpectadly raised an httpx.HTTPError: {e}"

    return cast(TFunction, new_func)


class Value:
    """Helper class to store a value in a pytest fixture."""

    value: Optional[str] = None

    def get(self):
        return self.value

    def set(self, value: Union[str, None]):
        self.value = value


TResourceRepresentation = TypeVar("TResourceRepresentation")
ResourceCreate = Callable[[], Awaitable[Optional[str]]]
ResourceGet = Callable[[Optional[str]], Awaitable[TResourceRepresentation]]
ResourceUpdate = Optional[Callable[[Optional[str]], Awaitable[None]]]
ResourceDelete = Callable[[Optional[str]], Awaitable[None]]


class ResourceLifeCycleTest(ABC, Generic[TResourceRepresentation]):
    """Base class for testing the lifecycle of a keycloak resource.

    It tests the lifecycle of a keycloak resource by calling the create, get,
    update and delete methods and passing the identifier accross the lifecycle.

    The identifier may be ommited in which case its only use is to setup the
    dependency chain between tests.

    Test classes which inherit from this class must implement the following
    class scoped fixtures (methods decorated with @pytest.fixture(scope="class")):
    - create: returns a function that creates a resource and returns its identifier.
    - get: returns a function that gets a resource.
    - update: returns a function that updates a resource. May return None if not applicable.
    - delete: returns a function that deletes a resource.
    """

    @classmethod
    def dependency_name(
        cls,
        test_type: Literal["create", "get", "update", "delete"],
        scope: Scope = "module",
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

    @pytest.fixture(scope="class")
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
                    f"""
                    Could not cleanup resource with id '{id}'
                    in {self.__class__.__module__}::{self.__class__.__name__}.
                    This could cause issues with other tests.
                """
                ).replace("\n", " ")
            )
            raise ex

    @assert_not_raises
    async def test_create(self, create: ResourceCreate, identifier: Value):
        """Test the create method."""
        identifier.set(await create())

    @depends(on="test_create", scope="class")
    @assert_not_raises
    async def test_get(self, get: ResourceGet, identifier: Value):
        """Test the get method."""
        await get(identifier.get())

    @depends(on="test_get", scope="class")
    @assert_not_raises
    async def test_update(self, update: Optional[ResourceUpdate], identifier: Value):
        """Test the update method."""
        if not update:
            pytest.skip(f"Update not implemented in {self.__class__.__name__}")
        await update(identifier.get())

    @depends(on="test_get", scope="class")
    @depends(on="test_update", scope="class", allow_skipped=True)
    @assert_not_raises
    async def test_delete(self, delete: ResourceDelete, identifier: Value):
        """Test the delete method."""
        await delete(identifier.get())
