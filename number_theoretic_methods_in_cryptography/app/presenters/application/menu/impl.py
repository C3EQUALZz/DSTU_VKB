from typing import override

from app.presenters.application.menu.base import IMenuPresenter
from app.presenters.application.primary.base import IMainPresenter
from app.views.application.container import AlgorithmContainer
from app.views.application.menu.base import IMainMenuView
from app.views.base import IView, T


class MenuPresenter(IMenuPresenter):
    def __init__(
            self,
            main_presenter: IMainPresenter,
            container: AlgorithmContainer,
    ) -> None:
        self._view: IMainMenuView | None = None
        self.main_presenter: IMainPresenter = main_presenter
        self.container: AlgorithmContainer = container
        self._map_name_and_view: dict[str, type[IView[T]]] = {}

    @override
    def attach_presenter(self, view: IMainMenuView) -> None:
        self._view: IMainMenuView = view

    def register_view(self, name: str, view: type[IView[T]]) -> None:
        self._map_name_and_view[name] = view

    @override
    def on_menu_selection(self, algorithm_key: str) -> None:
        view: IView[T] = self._map_name_and_view[algorithm_key](self.container) # type: ignore
        self.main_presenter.activate_presenter(algorithm_key, view)
        self.container.set_content(view)
