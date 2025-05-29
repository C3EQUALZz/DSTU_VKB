from typing import override

import customtkinter as ctk

from app.presenters.application.menu.base import IMenuPresenter
from app.views.application.menu.base import IMainMenuView


class MainMenuView(ctk.CTkFrame, IMainMenuView):
    def __init__(
            self,
            master,
            menu_presenter: IMenuPresenter
    ) -> None:
        super().__init__(master)
        self.presenter: IMenuPresenter = menu_presenter

        self.label = ctk.CTkLabel(self, text="Выберите алгоритм:")
        self.label.pack(pady=10)

    def register_button(self, name: str) -> None:
        button: ctk.CTkButton = ctk.CTkButton(
            self,
            text=name,
            command=lambda: self.presenter.on_menu_selection(name)
        )

        button.pack(pady=5)

    @override
    def show(self) -> None:
        self.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

    @override
    def hide(self) -> None:
        self.pack_forget()
