from typing import Any, Union
from dataclasses import asdict as _asdict


def remove_none(dictionary: dict[str, Any]) -> dict[str, Any]:
    def recurse(value: Union[dict, Any]):
        if type(value) is dict:
            return remove_none(value)
        else:
            return value

    return {k: recurse(v) for k, v in dictionary.items() if v is not None}


def asdict(dataclass) -> dict[str, Any]:
    return remove_none(_asdict(dataclass))
