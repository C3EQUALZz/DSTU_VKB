import customtkinter as ctk

from app.views.base import IView, T


class AlgorithmContainer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_view: IView | None = None

    def set_content(self, view: IView[T]) -> None:
        """Устанавливает текущее представление алгоритма"""
        if self.current_view:
            self.current_view.hide()

        self.current_view = view
        self.current_view.show()
