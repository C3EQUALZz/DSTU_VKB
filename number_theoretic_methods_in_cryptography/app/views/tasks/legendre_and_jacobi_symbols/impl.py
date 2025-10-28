from typing import Iterable, override

import customtkinter as ctk

from app.presenters.tasks.legendre_and_jacobi_symbols.base import ILegendreJacobiPresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.legendre_and_jacobi_symbols.base import ILegendreJacobiView


class LegendreJacobiView(ctk.CTkFrame, ILegendreJacobiView):
    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)

        self._presenter: ILegendreJacobiPresenter | None = None

        # Входные данные
        self.entry_numerator: ctk.CTkEntry = ctk.CTkEntry(self, width=100)
        self.entry_denominator: ctk.CTkEntry = ctk.CTkEntry(self, width=100)

        # Результаты
        self.result_text: ctk.CTkTextbox = ctk.CTkTextbox(self, wrap="word")

        # Размещение элементов
        self.__create_layout()

    @override
    def show(self) -> None:
        """Отображает представление"""
        self.pack(fill="both", expand=True)

    @override
    def hide(self) -> None:
        """Скрывает представление"""
        self.pack_forget()

    @override
    def attach_presenter(self, presenter: ILegendreJacobiPresenter) -> None:
        self._presenter: ILegendreJacobiPresenter = presenter
        button: ctk.CTkButton = ctk.CTkButton(self, text="Вычислить", command=self._presenter.calculate)
        button.grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

    @override
    def get_numerator(self) -> str:
        return self.entry_numerator.get()

    @override
    def get_denominator(self) -> str:
        return self.entry_denominator.get()

    @override
    def set_result(self, symbol_type: str, result: int | str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("0.0", "end")
        self.result_text.insert("end", f"Результат символа {symbol_type}: {result}\n")
        self.result_text.configure(state="disabled")

    @override
    def set_logs(self, logs: Iterable[str]) -> None:
        self.result_text.configure(state="normal")
        for log in logs:
            self.result_text.insert("end", log + "\n")
        self.result_text.configure(state="disabled")

    def __create_layout(self) -> None:
        # Настройка сетки для основного фрейма
        self.grid_columnconfigure((0, 1), weight=1)  # 2 равные колонки
        self.grid_rowconfigure(0, weight=0)  # Входные данные
        self.grid_rowconfigure(1, weight=0)  # Кнопка
        self.grid_rowconfigure(2, weight=1)  # Текстовое поле результатов

        # --- Входные данные ---
        # Числитель
        ctk.CTkLabel(self, text="Числитель (a)").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_numerator.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Знаменатель
        ctk.CTkLabel(self, text="Знаменатель (n)").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_denominator.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # --- Результаты ---
        self.result_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
