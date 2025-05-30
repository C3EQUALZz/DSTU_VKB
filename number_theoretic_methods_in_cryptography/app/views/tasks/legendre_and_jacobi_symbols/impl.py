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
        self.entry_a1: ctk.CTkEntry = ctk.CTkEntry(self, width=100)
        self.entry_b1: ctk.CTkEntry = ctk.CTkEntry(self, width=100)
        self.entry_a2: ctk.CTkEntry = ctk.CTkEntry(self, width=100)
        self.entry_b2: ctk.CTkEntry = ctk.CTkEntry(self, width=100)

        # Результаты
        self.legendre_text: ctk.CTkTextbox = ctk.CTkTextbox(self, wrap="word")
        self.jacobi_text: ctk.CTkTextbox = ctk.CTkTextbox(self, wrap="word")

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
        button.grid(row=2, column=0, columnspan=4, pady=15, sticky="ew")

    @override
    def get_a1(self) -> str:
        return self.entry_a1.get()

    @override
    def get_b1(self) -> str:
        return self.entry_b1.get()

    @override
    def get_a2(self) -> str:
        return self.entry_a2.get()

    @override
    def get_b2(self) -> str:
        return self.entry_b2.get()

    @override
    def set_legendre_result(self, result: int) -> None:
        self.legendre_text.configure(state="normal")
        self.legendre_text.delete("0.0", "end")
        self.legendre_text.insert("end", f"Результат символа Лежандра: {result if result != -2 else "Невозможно посчитать"}\n")
        self.legendre_text.configure(state="disabled")

    @override
    def set_legendre_logs(self, logs: Iterable[str]) -> None:
        self.legendre_text.configure(state="normal")
        for log in logs:
            self.legendre_text.insert("end", log + "\n")
        self.legendre_text.configure(state="disabled")

    @override
    def set_jacobi_result(self, result: int) -> None:
        self.jacobi_text.configure(state="normal")
        self.jacobi_text.delete("0.0", "end")
        self.jacobi_text.insert("end", f"Результат символа Якоби: {result}\n")
        self.jacobi_text.configure(state="disabled")

    @override
    def set_jacobi_logs(self, logs: Iterable[str]) -> None:
        self.jacobi_text.configure(state="normal")
        for log in logs:
            self.jacobi_text.insert("end", log + "\n")
        self.jacobi_text.configure(state="disabled")

    def __create_layout(self) -> None:
        # Настройка сетки для основного фрейма
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)  # 4 равные колонки
        self.grid_rowconfigure(0, weight=0)  # Входные данные
        self.grid_rowconfigure(1, weight=0)  # Кнопка
        self.grid_rowconfigure(2, weight=0)  # Заголовки результатов
        self.grid_rowconfigure(3, weight=1)  # Текстовые поля результатов

        # --- Входные данные ---
        # a1
        ctk.CTkLabel(self, text="a1").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_a1.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # b1
        ctk.CTkLabel(self, text="b1").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_b1.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # a2
        ctk.CTkLabel(self, text="a2").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_a2.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # b2
        ctk.CTkLabel(self, text="b2").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_b2.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # --- Результаты ---
        # Символ Лежандра
        self.legendre_text.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        # Символ Якоби
        self.jacobi_text.grid(row=4, column=2, columnspan=2, sticky="nsew", padx=10, pady=5)

        # --- Растяжение текстовых полей ---
        self.grid_rowconfigure(4, weight=1)
