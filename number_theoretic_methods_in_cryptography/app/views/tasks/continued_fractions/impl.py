import customtkinter as ctk

from app.presenters.tasks.continued_fractions.base import IContinuedFractionPresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.continued_fractions.base import IContinuedFractionView
from typing import Iterable, override


class ContinuedFractionView(ctk.CTkFrame, IContinuedFractionView):
    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)

        self._presenter: IContinuedFractionPresenter | None = None
        # Входные данные
        self.entry_a: ctk.CTkEntry = ctk.CTkEntry(self, width=100)
        self.entry_b: ctk.CTkEntry = ctk.CTkEntry(self, width=100)
        self.entry_m: ctk.CTkEntry = ctk.CTkEntry(self, width=100)

        # Результат
        self.solution_text: ctk.CTkTextbox = ctk.CTkTextbox(self, height=40, wrap="word")
        self.solution_text.configure(state="disabled")

        # Логи
        self.logs_text: ctk.CTkTextbox = ctk.CTkTextbox(self, wrap="word")

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
    def attach_presenter(self, presenter: IContinuedFractionPresenter) -> None:
        self._presenter: IContinuedFractionPresenter = presenter
        button = ctk.CTkButton(self, text="Решить", command=self._presenter.calculate)
        button.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

    @override
    def get_a(self) -> str:
        return self.entry_a.get()

    @override
    def get_b(self) -> str:
        return self.entry_b.get()

    @override
    def get_m(self) -> str:
        return self.entry_m.get()

    @override
    def set_solution(self, solution: int) -> None:
        self.solution_text.configure(state="normal")
        self.solution_text.delete("0.0", "end")
        self.solution_text.insert("end", f"x = {solution} (mod {self.get_m()})")
        self.solution_text.configure(state="disabled")

    @override
    def set_logs(self, logs: Iterable[str]) -> None:
        self.logs_text.configure(state="normal")
        self.logs_text.delete("0.0", "end")
        for log in logs:
            self.logs_text.insert("end", log + "\n")
        self.logs_text.configure(state="disabled")

    @override
    def clear(self) -> None:
        self.solution_text.configure(state="normal")
        self.solution_text.delete("0.0", "end")
        self.solution_text.configure(state="disabled")

        self.logs_text.configure(state="normal")
        self.logs_text.delete("0.0", "end")
        self.logs_text.configure(state="disabled")

    def __create_layout(self) -> None:
        # Настройка сетки
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)

        # Входные поля
        ctk.CTkLabel(self, text="a").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_a.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self, text="b").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_b.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self, text="m").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_m.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Результат
        ctk.CTkLabel(self, text="Решение:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.solution_text.grid(row=3, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Логи
        self.logs_text.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
