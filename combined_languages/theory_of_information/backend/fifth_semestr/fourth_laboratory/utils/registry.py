from typing import Mapping, AnyStr


class Singleton:
    _instance = None

    def __new__(cls) -> "Singleton":
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Registry(Singleton):
    __registry = {}

    @classmethod
    def log(cls, state: AnyStr, comment: AnyStr) -> None:
        cls.__registry[state] = comment

    @classmethod
    def get_all_info(cls) -> Mapping[AnyStr, AnyStr]:
        return cls.__registry

    @classmethod
    def clear(cls) -> None:
        cls.__registry.clear()
