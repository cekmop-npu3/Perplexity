from typing import Any


class Attr:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __get__(self, instance, owner) -> Any:
        return self.value

    def __set__(self, instance, value):
        raise AttributeError("Can't set attribute")

    def __repr__(self) -> str:
        return f'{self.value}'


def isDunderMethod(method: str) -> bool:
    return True if hasattr(object, method) or method.startswith('__') else False


class ReadOnlyMeta(type):
    def __new__(mcs, name, bases, attrs) -> object:
        return super().__new__(mcs, name, bases,
                               {key: (value if isDunderMethod(key) else Attr(value)) for key, value in attrs.items()})

    def __call__(cls, *args, **kwargs) -> object:
        instance = super().__call__(*args, **kwargs)
        [setattr(cls, key, Attr(value)) for key, value in instance.__dict__.items()]
        return instance

    def __setattr__(cls, key, value) -> None:
        if hasattr(cls, key):
            raise AttributeError("Can't set attribute")
        super().__setattr__(key, value)


class ReadOnly(metaclass=ReadOnlyMeta):
    """
    Класс ReadOnly делает аттрибуты класса доступными только для чтения
    и применяет эти свойства как к классам, так и к экземплярам классов

    Применение:

    class ClassName(ReadOnly):
        arg1 = 10  # Аттрибут для чтения
        arg2 = 3.3  # Аттрибут для чтения
        def __init__(self, arg3):
            self.arg3 = arg3  # Аттрибут для чтения

    # Это работает
    print(ClassName.arg)
    print(ClassName(arg3=87).arg2)
    print(ClassName(arg3=87).arg3)

    # А это вызовет AttributeError
    Classname.arg = 13
    Classname(arg3=87).arg2 = 27
    Classname(arg3=87).arg3 = 27

    Важно! При наследовании класса, наследующего ReadOnly,
    все аттрибуты нового класса тоже будут доступны только для чтения
    """
