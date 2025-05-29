import customtkinter as ctk
from app.presenters.application import MainPresenter
from app.views.application.menu import MainMenuView
from app.views.application.container import AlgorithmContainer
from app.presenters.algorithm1 import Algorithm1Presenter
from app.presenters.algorithm2 import Algorithm2Presenter

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MVP Multi-Algorithm App")
        self.geometry("1000x600")

        # Инициализируем Presenter
        self.main_presenter = MainPresenter()
        self.main_presenter.register_presenter("algorithm1", Algorithm1Presenter)
        self.main_presenter.register_presenter("algorithm2", Algorithm2Presenter)

        # Контейнеры
        self.menu = MainMenuView(self, self.on_menu_selection)
        self.container = AlgorithmContainer(self)

        # Отображаем элементы
        self.menu.show()
        self.container.show()

    def on_menu_selection(self, algorithm_key: str):
        """Обработчик выбора алгоритма"""
        if algorithm_key == "algorithm1":
            view = Algorithm1View(self.container)
        elif algorithm_key == "algorithm2":
            view = Algorithm2View(self.container)
        else:
            return

        self.main_presenter.activate_presenter(algorithm_key, view)
        self.container.set_content(view)

if __name__ == "__main__":
    app = Application()
    app.mainloop()