import customtkinter as ctk

from app.views.base import IView


class AlgorithmContainer(ctk.CTkFrame, IView):
    def __init__(self, master):
        super().__init__(master)
        self.current_view: IView | None = None

    def set_content(self, view: IView) -> None:
        """Устанавливает текущее представление алгоритма"""
        if self.current_view:
            self.current_view.hide()

        self.current_view = view
        self.current_view.show()

    def show(self) -> None:
        self.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def hide(self) -> None:
        self.pack_forget()
