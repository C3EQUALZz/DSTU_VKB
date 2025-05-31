from typing import override, Iterable

import customtkinter as ctk

from app.presenters.tasks.quadratic_comparison.base import IQuadraticComparisonPresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.quadratic_comparison.base import IQuadraticComparisonView


class QuadraticComparisonView(ctk.CTkFrame, IQuadraticComparisonView):
    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)

        self._presenter: IQuadraticComparisonPresenter | None = None
        # Поля ввода
        self.entry_number = ctk.CTkEntry(self, width=150, placeholder_text="Число a")
        self.entry_prime = ctk.CTkEntry(self, width=150, placeholder_text="Простое число p")

        # Результаты
        self.label_result = ctk.CTkLabel(self, text="", wraplength=400)

        # Логи
        self.log_box = ctk.CTkTextbox(self, wrap="word", height=200)
        self.log_box.configure(state="disabled")

        # Упаковка элементов
        self._create_layout()

    @override
    def show(self) -> None:
        self.pack(fill="both", expand=True)

    @override
    def hide(self) -> None:
        self.pack_forget()

    @override
    def attach_presenter(self, presenter: IQuadraticComparisonPresenter) -> None:
        self._presenter: IQuadraticComparisonPresenter = presenter

        button_calculate: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Вычислить",
            command=self._presenter.calculate
        )

        button_calculate.pack(pady=10)

    def _create_layout(self) -> None:
        # Ввод a
        self.entry_number.pack(side="left", padx=5)

        # Ввод p
        self.entry_prime.pack(side="left", padx=5)

        # Результат
        self.label_result.pack(pady=10)

        # Логи
        self.log_box.pack(fill="both", expand=True)

    @override
    def get_number(self) -> str:
        return self.entry_number.get()

    @override
    def get_prime(self) -> str:
        return self.entry_prime.get()

    @override
    def set_result(self, result: tuple[int, int]) -> None:
        """Устанавливает результат в виде корней сравнения"""
        root1, root2 = result
        self.label_result.configure(text=f"Корни: ({root1}, {root2})")

    @override
    def show_logs(self, logs: Iterable[str]) -> None:
        """Отображает логи вычисления"""
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        for line in logs:
            self.log_box.insert("end", line + "\n")
        self.log_box.configure(state="disabled")
