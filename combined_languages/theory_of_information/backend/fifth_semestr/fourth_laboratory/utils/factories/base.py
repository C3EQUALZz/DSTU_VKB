from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any, Final

PATH_TO_MODELS: Final = "combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models."


class Factory(ABC):
    @classmethod
    @abstractmethod
    def create(cls, matrix, matrix_type: str) -> Any:
        ...


class RegistryFactory(Factory, ABC):
    _registry = {}

    # NOTE: я не придумал как сделать нормально без динамического импорта.
    # У Python есть проблема с циклическими импортами.
    # В случае бы GSystematic и Hsystematic просто импортировали бы друг друга, а это плохо
    @classmethod
    def register(cls, matrix_type: str, matrix_class_name: str) -> None:
        module_name, class_name = (PATH_TO_MODELS + matrix_class_name).rsplit('.', 1)
        matrix_class = getattr(import_module(module_name), class_name)
        cls._registry[matrix_type] = matrix_class

