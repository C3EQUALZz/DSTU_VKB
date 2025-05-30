from typing import override, Iterable

import customtkinter as ctk

from app.presenters.tasks.comparison_of_the_first_degree.base import IComparisonOfFirstDegreePresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.comparison_of_the_first_degree.base import IComparisonOfFirstDegreeView


class ComparisonOfFirstDegreeView(ctk.CTkFrame, IComparisonOfFirstDegreeView):
    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)
        self._presenter: IComparisonOfFirstDegreePresenter | None = None
        self._entries: dict[str, ctk.CTkEntry] = {}

        self.__create_input_fields()
        self.__create_log_box()

    @override
    def attach_presenter(self, presenter: IComparisonOfFirstDegreePresenter) -> None:
        self._presenter: IComparisonOfFirstDegreePresenter = presenter

        button: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Решить",
            command=self._presenter.solve_congruence
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
    def get_a(self) -> str:
        return self._entries["a"].get()

    @override
    def get_b(self) -> str:
        return self._entries["b"].get()

    @override
    def get_m(self) -> str:
        return self._entries["m"].get()

    @override
    def show_logs(self, logs: Iterable[str]) -> None:
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        for line in logs:
            self.log_box.insert("end", line + "\n")
        self.log_box.configure(state="disabled")

    def __create_input_fields(self):
        input_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20, fill="x")

        fields: list[tuple[str, str]] = [
            ("a", "Коэффициент a"),
            ("b", "Свободный член b"),
            ("m", "Модуль m")
        ]

        for key, label in fields:
            ctk.CTkLabel(input_frame, text=label).pack(pady=5)
            self._entries[key] = ctk.CTkEntry(input_frame, width=150)
            self._entries[key].pack(pady=5)

    def __create_log_box(self) -> None:
        log_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        log_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.log_box: ctk.CTkTextbox = ctk.CTkTextbox(log_frame, wrap="word")
        self.log_box.pack(fill="both", expand=True)
        self.log_box.configure(state="disabled")
