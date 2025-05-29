from typing import Dict, Type
from app.presenters.base import IPresenter
from app.views.base import IView


class MainPresenter:
    def __init__(self):
        self.current_presenter: IPresenter | None = None
        self.presenter_map: Dict[str, Type[IPresenter]] = {}

    def register_presenter(self, key: str, presenter_class: Type[IPresenter]) -> None:
        """Регистрирует Presenter для пункта меню"""
        self.presenter_map[key] = presenter_class

    def activate_presenter(self, key: str, view: IView) -> None:
        """Активирует Presenter по ключу"""
        if key not in self.presenter_map:
            raise ValueError(f"Presenter {key} не зарегистрирован")

        # Создаем новый Presenter
        new_presenter: IPresenter = self.presenter_map[key]()

        self.current_presenter = new_presenter
        self.current_presenter.attach_view(view)
        self.current_presenter.on_activate()
