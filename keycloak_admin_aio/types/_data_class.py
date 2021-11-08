from __future__ import annotations

from typing import Any, TypeVar

from dacite.core import from_dict

from keycloak_admin_aio._lib.utils import asdict


class DataClass:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def to_dict_list(representation_list: list[T]) -> list[dict[str, Any]]:
        return list(
            map(lambda representation: representation.to_dict(), representation_list)
        )

    @classmethod
    def from_dict(cls, dictionary: dict):
        return from_dict(data_class=cls, data=dictionary)

    @classmethod
    def from_list(cls, _list: list[dict]):
        return list(map(cls.from_dict, _list))


T = TypeVar("T", bound=DataClass)
