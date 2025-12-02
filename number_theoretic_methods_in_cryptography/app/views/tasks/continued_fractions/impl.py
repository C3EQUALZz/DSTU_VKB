import customtkinter as ctk

from app.presenters.tasks.continued_fractions.base import IContinuedFractionPresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.continued_fractions.base import IContinuedFractionView
from typing import Iterable, override


class ContinuedFractionView(ctk.CTkFrame, IContinuedFractionView):
    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)

        self._presenter: IContinuedFractionPresenter | None = None
        
        # Создание элементов интерфейса
        self.__create_input_fields()
        self.__create_solution_field()
        self.__create_log_box()

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
        
        button: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Решить",
            command=self._presenter.calculate
        )
        button.pack(pady=10)

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

    def __create_input_fields(self) -> None:
        """Создает поля ввода сверху вниз: a, b, m"""
        input_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20, fill="x")

        # Поле a
        ctk.CTkLabel(input_frame, text="a").pack(pady=5)
        self.entry_a: ctk.CTkEntry = ctk.CTkEntry(input_frame, width=150)
        self.entry_a.pack(pady=5)

        # Поле b
        ctk.CTkLabel(input_frame, text="b").pack(pady=5)
        self.entry_b: ctk.CTkEntry = ctk.CTkEntry(input_frame, width=150)
        self.entry_b.pack(pady=5)

        # Поле m
        ctk.CTkLabel(input_frame, text="m").pack(pady=5)
        self.entry_m: ctk.CTkEntry = ctk.CTkEntry(input_frame, width=150)
        self.entry_m.pack(pady=5)

    def __create_solution_field(self) -> None:
        """Создает поле для вывода решения (меньшего размера)"""
        solution_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        solution_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(solution_frame, text="Решение:").pack(pady=5)
        self.solution_text: ctk.CTkTextbox = ctk.CTkTextbox(solution_frame, height=30, wrap="word")
        self.solution_text.pack(pady=5, fill="x")
        self.solution_text.configure(state="disabled")

    def __create_log_box(self) -> None:
        """Создает область для вывода логов"""
        log_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        log_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.logs_text: ctk.CTkTextbox = ctk.CTkTextbox(log_frame, wrap="word")
        self.logs_text.pack(fill="both", expand=True)
        self.logs_text.configure(state="disabled")
