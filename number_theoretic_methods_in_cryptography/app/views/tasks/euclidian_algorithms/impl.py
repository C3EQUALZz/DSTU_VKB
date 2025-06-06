import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from typing import override
from app.presenters.tasks.euclidian_algorithms.base import IGCDPresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.euclidian_algorithms.base import IGCDView


class GCDView(ctk.CTkFrame, IGCDView):
    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)
        self.presenter: IGCDPresenter | None = None

        self._create_input_frame()
        self._create_strategy_selector()
        self._create_output_tabs()

    @override
    def attach_presenter(self, presenter: IGCDPresenter) -> None:
        self.presenter = presenter
        self._create_run_button()

    @override
    def set_strategies(self, strategies: list[str]) -> None:
        self.strategy_menu.configure(values=strategies)
        if strategies:
            self.strategy_var.set(strategies[0])

    @override
    def get_inputs(self) -> tuple[str, str]:
        return self.entry_a.get(), self.entry_b.get()

    @override
    def get_selected_strategy(self) -> str:
        return self.strategy_var.get()

    @override
    def display_result(self, result: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", result)
        self.result_text.configure(state="disabled")

    @override
    def display_logs(self, logs: list[str]) -> None:
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", "\n".join(logs))
        self.log_text.configure(state="disabled")

    @override
    def show_error(self, message: str) -> None:
        CTkMessagebox(title="Ошибка", message=message, icon="cancel", option_1="ОК")

    @override
    def show(self) -> None:
        """Отображает представление"""
        self.pack(fill="both", expand=True)

    @override
    def hide(self) -> None:
        """Скрывает представление"""
        self.pack_forget()

    def _create_run_button(self) -> None:
        self.run_button = ctk.CTkButton(
            self,
            text="Вычислить",
            command=self.presenter.on_calculate
        )
        self.run_button.pack(pady=10)

    def _create_input_frame(self) -> None:
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        self.label_a = ctk.CTkLabel(self.input_frame, text="Число a:")
        self.label_a.grid(row=0, column=0, padx=10, pady=5)
        self.entry_a = ctk.CTkEntry(self.input_frame, placeholder_text="Введите число a")
        self.entry_a.grid(row=0, column=1, padx=10, pady=5)

        self.label_b = ctk.CTkLabel(self.input_frame, text="Число b:")
        self.label_b.grid(row=1, column=0, padx=10, pady=5)
        self.entry_b = ctk.CTkEntry(self.input_frame, placeholder_text="Введите число b")
        self.entry_b.grid(row=1, column=1, padx=10, pady=5)

    def _create_strategy_selector(self) -> None:
        self.strategy_frame = ctk.CTkFrame(self)
        self.strategy_frame.pack(pady=10, padx=20, fill="x")

        self.strategy_var = ctk.StringVar()
        self.strategy_label = ctk.CTkLabel(self.strategy_frame, text="Выберите алгоритм:")
        self.strategy_label.pack(side="left", padx=10)

        self.strategy_menu = ctk.CTkOptionMenu(
            self.strategy_frame,
            values=[],
            variable=self.strategy_var
        )
        self.strategy_menu.pack(side="left", padx=10)

    def _create_output_tabs(self) -> None:
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        self.tabview.add("Логи")
        self.tabview.add("Результат")

        # Логи
        self.log_text = ctk.CTkTextbox(self.tabview.tab("Логи"), wrap="word")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")

        # Результат
        self.result_text = ctk.CTkTextbox(self.tabview.tab("Результат"), wrap="word")
        self.result_text.pack(fill="both", expand=True)
        self.result_text.configure(state="disabled")


