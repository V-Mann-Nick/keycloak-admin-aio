import uuid
from dataclasses import asdict as _asdict
from typing import Any, Optional, TypeVar, Union

import httpx


def remove_none(dictionary: dict[str, Any]) -> dict[str, Any]:
    def recurse(value: Union[dict, Any]):
        if type(value) is dict:
            return remove_none(value)
        else:
            return value

    return {k: recurse(v) for k, v in dictionary.items() if v is not None}


def asdict(dataclass) -> dict[str, Any]:
    return remove_none(_asdict(dataclass))


def is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def get_resource_id_in_location_header(
    response: httpx.Response, is_no_uuid=False
) -> str:
    location_header = response.headers.get("location")
    if not location_header or type(location_header) != str:
        raise Exception("The response headers didn't include location.")
    resource_id = location_header.split("/").pop()
    is_correct_type = type(resource_id) == str and (is_no_uuid or is_uuid(resource_id))
    if not is_correct_type:
        raise Exception("Resource id couldn't be found in location header.")
    return resource_id


T = TypeVar("T")


def cast_non_optional(arg: Optional[T]) -> T:
    assert arg is not None
    return arg
