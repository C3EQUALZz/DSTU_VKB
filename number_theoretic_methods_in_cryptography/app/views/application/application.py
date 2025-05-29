import customtkinter as ctk

from app.presenters.application.menu.impl import MenuPresenter
from app.presenters.application.primary.base import IMainPresenter
from app.presenters.application.primary.impl import MainPresenter
from app.presenters.tasks.base import ITaskPresenter
from app.views.application.container import AlgorithmContainer
from app.views.application.menu.impl import MainMenuView
from app.views.base import IView


class Application(ctk.CTk):
    def __init__(self, tasks: dict[str, tuple[type[ITaskPresenter], type[IView]]]) -> None:
        super().__init__()
        self.tasks = tasks
        self.title("Данил Ковалев ВКБ42 Теоретико-числовые методы в криптографии")
        self.geometry("1000x700")

        self.container: AlgorithmContainer = AlgorithmContainer(self)
        self.main_presenter: IMainPresenter = MainPresenter()
        self.menu_presenter = MenuPresenter(
            main_presenter=self.main_presenter,
            container=self.container,
        )
        self.menu = MainMenuView(self, self.menu_presenter)
        self.menu_presenter.attach_presenter(self.menu)

        for name, (presenter, view) in self.tasks.items():
            self.main_presenter.register_presenter(name, presenter)  # type: ignore
            self.menu.register_button(name)
            self.menu_presenter.register_view(name=name, view=view)

        # Отображаем элементы
        self.menu.pack(side="left", fill="y", padx=10, pady=10)
        self.container.pack(side="right", fill="both", expand=True, padx=10, pady=10)
