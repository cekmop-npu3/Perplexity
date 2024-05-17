from typing import Any, Iterable


class Format:
    def __init__(self, obj: Any) -> None:
        self.obj = obj


class CustomDict(dict):
    def __init__(self, kwargs) -> None:
        super().__init__(kwargs)

    def __getattr__(self, item) -> Any:
        return super().get(item)

    def __setattr__(self, key, value) -> None:
        return super().__setitem__(key, value)


class DictMeta(type):
    def __new__(mcs, name, bases, attrs) -> CustomDict:
        return CustomDict(dict(map(lambda item: (item[0].replace('_', '-'), item[1].obj) if isinstance(item[1], Format) else (item[0], item[1]), filter(lambda item: not hasattr(object, item[0]), attrs.items()))))

    def __getitem__(self, key: Any) -> Any:
        pass

    def __setitem__(self, key: Any, value: Any) -> None:
        pass

    def __delitem__(self, key: Any) -> None:
        pass

    def __contains__(self, key: Any) -> bool:
        pass

    def __len__(self) -> int:
        pass

    def __iter__(self) -> iter:
        pass

    def get(self, key: Any, default: Any = None) -> Any:
        pass

    def clear(self) -> None:
        pass

    def copy(self) -> dict:
        pass

    def items(self) -> list[tuple]:
        pass

    def keys(self) -> list:
        pass

    def pop(self, key: Any, default=None) -> Any:
        pass

    def popitem(self) -> tuple:
        pass

    def setdefault(self, key: Any, default=None) -> Any:
        pass

    def update(self, other: Iterable) -> None:
        pass

    def values(self) -> list:
        pass
