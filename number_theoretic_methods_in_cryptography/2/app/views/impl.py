from typing import Iterable

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from app.presenters.interface import PresenterInterface
from app.views.interface import ViewInterface


class EulerView(ctk.CTk, ViewInterface):
    def __init__(self, presenter: PresenterInterface) -> None:
        super().__init__()
        self.presenter = presenter
        self.title("Сравнение по модулю")
        self.geometry("1000x650")  # Увеличена ширина окна

        # Настройка темы
        ctk.set_appearance_mode("System")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue, dark-blue, green

        # Поля ввода
        self._create_input_section()

        # Кнопка вычисления
        self.btn_calculate = ctk.CTkButton(
            self,
            text="Вычислить",
            command=self._on_calculate
        )
        self.btn_calculate.pack(pady=10)

        # Результаты
        self._create_result_section()

        # Логи
        self._create_log_section()

    def _create_input_section(self) -> None:
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(padx=20, pady=10, fill="x")  # Добавлено fill="x"

        # Первое число
        ctk.CTkLabel(input_frame, text="Первое число:").grid(row=0, column=0, padx=5, sticky="e")
        self.entry_a = ctk.CTkEntry(input_frame, width=150)  # Увеличена ширина
        self.entry_a.grid(row=0, column=1, padx=5)
        self.entry_k = ctk.CTkEntry(input_frame, width=150)  # Увеличена ширина
        self.entry_k.grid(row=0, column=2, padx=5)

        # Второе число
        ctk.CTkLabel(input_frame, text="Второе число:").grid(row=1, column=0, padx=5, sticky="e")
        self.entry_b = ctk.CTkEntry(input_frame, width=150)  # Увеличена ширина
        self.entry_b.grid(row=1, column=1, padx=5)
        self.entry_m = ctk.CTkEntry(input_frame, width=150)  # Увеличена ширина
        self.entry_m.grid(row=1, column=2, padx=5)

        # Модуль
        ctk.CTkLabel(input_frame, text="Модуль n:").grid(row=2, column=0, padx=5, sticky="e")
        self.entry_n = ctk.CTkEntry(input_frame, width=150)  # Увеличена ширина
        self.entry_n.grid(row=2, column=1, padx=5)

    def _create_result_section(self) -> None:
        result_frame = ctk.CTkFrame(self)
        result_frame.pack(padx=40, pady=10, fill="x", expand=True)  # Добавлено fill="x"

        ctk.CTkLabel(result_frame, text="Результаты:").pack()
        self.lbl_result1 = ctk.CTkLabel(result_frame, text="", wraplength=300)  # Добавлено обрезание текста
        self.lbl_result1.pack()
        self.lbl_result2 = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.lbl_result2.pack()
        self.lbl_sum_result = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.lbl_sum_result.pack()

    def _create_log_section(self) -> None:
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(padx=20, pady=10, fill="both", expand=True)

        ctk.CTkLabel(log_frame, text="Логи:").pack()
        self.txt_logs = ctk.CTkTextbox(log_frame, width=600, wrap="word")  # Установлена ширина
        self.txt_logs.pack(fill="both", expand=True)
        self.txt_logs.configure(state="disabled")

    def get_a(self) -> int:
        return int(self.entry_a.get())

    def get_b(self) -> int:
        return int(self.entry_b.get())

    def get_k(self) -> int:
        return int(self.entry_k.get())

    def get_m(self) -> int:
        return int(self.entry_m.get())

    def get_n(self) -> int:
        return int(self.entry_n.get())

    def set_result1(self, text: str) -> None:
        self.lbl_result1.configure(text=f"Результат 1: {text}")

    def set_result2(self, text: str) -> None:
        self.lbl_result2.configure(text=f"Результат 2: {text}")

    def set_sum_result(self, text: str) -> None:
        self.lbl_sum_result.configure(text=f"Сумма результатов: {text}")

    def show_logs(self, logs: Iterable[str]) -> None:
        self.txt_logs.configure(state="normal")
        self.txt_logs.delete("0.0", "end")
        for line in logs:
            self.txt_logs.insert("end", line + "\n")
        self.txt_logs.configure(state="disabled")

    def show_error(self, message: str) -> None:
        CTkMessagebox(title="Ошибка", message=message, icon="cancel", option_1="ОК")

    def _on_calculate(self) -> None:
        self.presenter.calculate()