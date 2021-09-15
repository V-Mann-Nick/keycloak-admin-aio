from typing import Any, TypeVar
from .utils import asdict
from dacite import from_dict

T = TypeVar("T")


class DataClass:
    def to_dict(self):
        return asdict(self)

    @staticmethod
    def to_dict_list(_list: list[T]) -> list[T]:
        return list(map(lambda t: t.to_dict(), _list))

    @classmethod
    def from_dict(cls, dictionary: dict):
        return from_dict(data_class=cls, data=dictionary)

    @classmethod
    def from_list(cls, _list: list[dict]):
        return list(map(cls.from_dict, _list))
