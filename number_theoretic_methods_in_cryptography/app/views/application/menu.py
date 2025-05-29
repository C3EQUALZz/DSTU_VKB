import customtkinter as ctk
from app.views.base import IView


class MainMenuView(ctk.CTkFrame, IView):
    def __init__(self, master, on_algorithm_selected):
        super().__init__(master)
        self.on_algorithm_selected = on_algorithm_selected

        self.label = ctk.CTkLabel(self, text="Выберите алгоритм:")
        self.label.pack(pady=10)

        self.btn_alg1 = ctk.CTkButton(
            self,
            text="Алгоритм 1",
            command=lambda: on_algorithm_selected("algorithm1")
        )
        self.btn_alg1.pack(pady=5)

        self.btn_alg2 = ctk.CTkButton(
            self,
            text="Алгоритм 2",
            command=lambda: on_algorithm_selected("algorithm2")
        )

        self.btn_alg2.pack(pady=5)

    def show(self) -> None:
        self.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

    def hide(self) -> None:
        self.pack_forget()
