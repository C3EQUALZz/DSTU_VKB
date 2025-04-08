from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any, Final, Literal, List

PATH_TO_MODELS: Final[str] = "app.domain.entities.block_codes."


class Factory(ABC):
    @classmethod
    @abstractmethod
    def create(cls, matrix: List[List[int]], matrix_type: Literal["G", "H"]) -> Any:
        """
        Базовый метод для создания фабрики, который каждый класс должен переопределить для своего случая.
        :param matrix: Матрица, которая введена пользователем.
        :param matrix_type: Тип матрицы, который определил пользователь (G или H).
        :returns: Возвращает нужный тип матрицы, который определили дочерние классы.
        """
        raise NotImplementedError


class RegistryFactory(Factory, ABC):
    _registry = {}

    # NOTE: я не придумал как сделать нормально без динамического импорта.
    # У Python есть проблема с циклическими импортами.
    # В случае бы GSystematic и Hsystematic просто импортировали бы друг друга, а это плохо
    @classmethod
    def register(cls, matrix_type: Literal["G", "H"], matrix_class_name: str) -> None:
        """
        Метод, который регистрирует зависимости для будущего создания с помощью фабрики.
        :param matrix_type: Тип матрицы для динамического импорта.
        :param matrix_class_name: Класс матрицы (путь относительно папки models) для импорта
        """
        module_name, class_name = (PATH_TO_MODELS + matrix_class_name).rsplit('.', 1)
        matrix_class = getattr(import_module(module_name), class_name)
        cls._registry[matrix_type] = matrix_class
