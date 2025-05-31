from typing import Iterable, override, Final

import customtkinter as ctk

from app.presenters.tasks.legendre_symbol.base import ILegendrePresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.legendre_symbol.base import ILegendreView


class LegendreView(ctk.CTkFrame, ILegendreView):
    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)

        self._presenter: ILegendrePresenter | None = None
        self.__entry_variant: Final[ctk.CTkEntry] = ctk.CTkEntry(self, width=100)
        self.__label_n: Final[ctk.CTkLabel] = ctk.CTkLabel(self, text="n = ")
        self.__label_p: Final[ctk.CTkLabel] = ctk.CTkLabel(self, text="p = ")
        self.__legendre_text: Final[ctk.CTkTextbox] = ctk.CTkTextbox(self, wrap="word")

        self.__create_layout()

    @override
    def attach_presenter(self, presenter: ILegendrePresenter) -> None:
        self._presenter: ILegendrePresenter = presenter

        button: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Вычислить",
            command=self._presenter.calculate
        )

        button.pack(pady=10)

    @override
    def show(self) -> None:
        """Отображает представление"""
        self.pack(fill="both", expand=True)

    @override
    def hide(self) -> None:
        """Скрывает представление"""
        self.pack_forget()

    @override
    def get_variant_number(self) -> int:
        return self.__entry_variant.get()

    @override
    def set_n(self, n: int) -> None:
        self.__label_n.configure(text=f"n = {n}")

    @override
    def set_p(self, p: int) -> None:
        self.__label_p.configure(text=f"p = {p}")

    @override
    def set_legendre_result(self, n: int, p: int, result: int) -> None:
        self.__legendre_text.configure(state="normal")
        self.__legendre_text.delete("0.0", "end")
        self.__legendre_text.insert("end", f"Символ Лежандра ({n}/{p}) = {result}\n")
        self.__legendre_text.configure(state="disabled")

    @override
    def set_logs(self, logs: Iterable[str]) -> None:
        self.__legendre_text.configure(state="normal")
        for log in logs:
            self.__legendre_text.insert("end", log + "\n")
        self.__legendre_text.configure(state="disabled")

    def __create_layout(self) -> None:
        self.__entry_variant.pack(side="left", padx=5)
        self.__label_n.pack(pady=5)
        self.__label_p.pack(pady=5)
        self.__legendre_text.pack(fill="both", expand=True)
