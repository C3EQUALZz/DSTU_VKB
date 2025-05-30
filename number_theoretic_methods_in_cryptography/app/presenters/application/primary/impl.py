from typing import Dict, Type

from app.presenters.application.primary.base import IMainPresenter
from app.presenters.tasks.base import ITaskPresenter
from app.views.tasks.base import ITaskView, T


class MainPresenter(IMainPresenter):
    def __init__(self) -> None:
        self.current_presenter: ITaskPresenter | None = None
        self.presenter_map: Dict[str, Type[ITaskPresenter]] = {}

    def register_presenter(self, key: str, presenter_class: Type[ITaskPresenter]) -> None:
        """Регистрирует Presenter для пункта меню"""
        self.presenter_map[key] = presenter_class

    def activate_presenter(self, key: str, view: ITaskView[T]) -> None:
        """Активирует Presenter по ключу"""
        if key not in self.presenter_map:
            raise ValueError(f"Presenter {key} не зарегистрирован")

        # Создаем новый Presenter
        new_presenter: ITaskPresenter = self.presenter_map[key]()

        self.current_presenter = new_presenter
        self.current_presenter.attach_view(view)
        view.attach_presenter(self.current_presenter)
        self.current_presenter.on_activate()
