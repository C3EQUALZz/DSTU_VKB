import customtkinter as ctk

from app.views.tasks.base import ITaskView, T


class AlgorithmContainer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_view: ITaskView | None = None

    def set_content(self, view: ITaskView[T]) -> None:
        """Устанавливает текущее представление алгоритма"""
        if self.current_view:
            self.current_view.hide()

        self.current_view = view
        self.current_view.show()
