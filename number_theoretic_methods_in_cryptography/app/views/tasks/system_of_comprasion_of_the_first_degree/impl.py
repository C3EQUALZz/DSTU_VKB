from typing import Iterable, override, Final

import customtkinter as ctk

from app.exceptions.views.system_of_comprasion_of_the_first_degree import IncorrectDataForEnteringTheNumberOfEquations
from app.presenters.tasks.system_of_comprasion_of_the_first_degree.base import ICRTPresenter
from app.views.application.container import AlgorithmContainer
from app.views.tasks.system_of_comprasion_of_the_first_degree.base import ICRTView


class CRTView(ctk.CTkFrame, ICRTView):
    MAX_EQUATIONS: Final[int] = 10  # Максимальное количество уравнений

    def __init__(self, master: AlgorithmContainer) -> None:
        super().__init__(master)

        self.__presenter: ICRTPresenter | None = None
        self.__equation_count: int = 3  # По умолчанию 3 уравнения
        self.__entries = []  # Список полей ввода (a_i, m_i, c_i)

        self.__input_frame = None
        self.__log_frame = None
        self.__button_frame = None  # Храним ссылку на фрейм кнопки
        self.__content_frame = None  # Теперь явно инициализируем

        # Основные разделы
        self.__button_frame = self.__create_button_frame()
        self.__selector_frame = self.__create_equation_selector()
        self.__content_frame = self.__create_content_frame()

        # Упаковка
        self.__button_frame.pack(pady=10)
        self.__selector_frame.pack(pady=10, padx=20, fill="x")
        self.__content_frame.pack(pady=(0, 10), padx=20, fill="both", expand=True)  # Не растягиваем вверху

    @override
    def attach_presenter(self, presenter: ICRTPresenter) -> None:
        self.__presenter = presenter
        self.__update_button_command()

    @override
    def show(self) -> None:
        """Отображает представление"""
        self.pack(fill="both", expand=True)

    @override
    def hide(self) -> None:
        """Скрывает представление"""
        self.pack_forget()

    @override
    def get_remainders(self) -> list[str]:
        """Возвращает список остатков"""
        return [entry[0].get() for entry in self.__entries]

    @override
    def get_moduli(self) -> list[str]:
        """Возвращает список модулей"""
        return [entry[1].get() for entry in self.__entries]

    @override
    def get_coefficients(self) -> list[str]:
        """Возвращает список коэффициентов при x"""
        return [entry[2].get() for entry in self.__entries]

    @override
    def show_logs(self, logs: Iterable[str]) -> None:
        self.__log_box.configure(state="normal")
        self.__log_box.delete("0.0", "end")

        for line in logs:
            self.__log_box.insert("end", line + "\n")

        self.__log_box.configure(state="disabled")

    def __create_equation_selector(self) -> ctk.CTkFrame:
        """Селектор количества уравнений"""
        selector_frame: ctk.CTkFrame = ctk.CTkFrame(self)

        ctk.CTkLabel(selector_frame, text="Количество уравнений:").pack(side="left", padx=5)

        equation_menu: ctk.CTkComboBox = ctk.CTkComboBox(
            selector_frame,
            values=[str(i) for i in range(2, self.MAX_EQUATIONS + 1)],
            variable=ctk.StringVar(value="3"),
            command=self.__on_equation_count_change
        )

        equation_menu.pack(side="left", padx=5)

        return selector_frame

    def __create_content_frame(self) -> ctk.CTkFrame:
        """Создает контент-фрейм с полями ввода и логами"""
        content_frame = ctk.CTkFrame(self)
        self.__create_input_fields(content_frame)
        self.__create_log_box(content_frame)
        return content_frame

    def __on_equation_count_change(self, value: str) -> None:
        """Обработчик изменения количества уравнений"""
        try:
            new_count: int = int(value)
            if new_count < 2 or new_count > self.MAX_EQUATIONS:
                raise ValueError("Количество уравнений должно быть от 2 до 10")
            self.__equation_count = new_count
        except Exception as e:
            raise IncorrectDataForEnteringTheNumberOfEquations(str(e))
        finally:
            self.__clear_input_fields()
            self.__refresh_content_frame()

    def __clear_input_fields(self) -> None:
        """Очищает поля ввода"""
        if self.__input_frame:
            self.__input_frame.destroy()
            self.__input_frame = None
        self.__entries.clear()

    def __refresh_content_frame(self) -> None:
        """Обновляет содержимое content_frame"""
        # Удаляем старый content_frame
        if self.__content_frame:
            self.__content_frame.destroy()

        # Создаем новый content_frame
        self.__content_frame = self.__create_content_frame()
        self.__content_frame.pack(pady=(0, 10), padx=20, fill="both", expand=True)  # Не растягиваем вверху

    def __create_input_fields(self, parent: ctk.CTkFrame) -> None:
        """Создаёт поля ввода в зависимости от количества уравнений"""
        self.__input_frame = ctk.CTkFrame(parent)
        self.__input_frame.pack(pady=5, fill="x")

        for i in range(self.__equation_count):
            row = ctk.CTkFrame(self.__input_frame)
            row.pack(pady=5)

            label_a = ctk.CTkLabel(row, text=f"b{i + 1}")
            label_a.pack(side="left", padx=5)
            entry_a = ctk.CTkEntry(row, width=80)
            entry_a.pack(side="left")

            label_c = ctk.CTkLabel(row, text=f"c{i + 1}")
            label_c.pack(side="left", padx=5)
            entry_c = ctk.CTkEntry(row, width=80)
            entry_c.pack(side="left")

            label_m = ctk.CTkLabel(row, text=f"m{i + 1}")
            label_m.pack(side="left", padx=5)
            entry_m = ctk.CTkEntry(row, width=80)
            entry_m.pack(side="left")

            self.__entries.append((entry_a, entry_m, entry_c))

    def __create_log_box(self, parent: ctk.CTkFrame) -> None:
        self.__log_frame = ctk.CTkFrame(parent)
        self.__log_frame.pack(pady=5, fill="both", expand=True)

        self.__log_box = ctk.CTkTextbox(self.__log_frame, wrap="word")
        self.__log_box.pack(fill="both", expand=True)
        self.__log_box.configure(state="disabled")

    def __create_button_frame(self) -> ctk.CTkFrame:
        """Создает фрейм для кнопки 'Решить'"""
        button_frame = ctk.CTkFrame(self)
        self.__solve_btn = ctk.CTkButton(
            button_frame,
            text="Решить",
            command=self.__presenter.solve_system if self.__presenter else None
        )
        self.__solve_btn.pack()
        return button_frame

    def __update_button_command(self) -> None:
        """Обновляет команду кнопки при изменении презентера"""
        if self.__solve_btn:
            self.__solve_btn.configure(command=self.__presenter.solve_system)