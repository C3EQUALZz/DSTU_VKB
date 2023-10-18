__all__ = ["Page"]

from PyQt6 import QtWidgets, QtCore


class Page(QtWidgets.QWidget):
    """
    Класс, который полностью описывает логику страницы
    """

    def __init__(self, num_lab):
        """
        Инициализация страницы.

        Args:
            num_lab (int): Номер лабораторной работы.
        """
        super().__init__()
        # Создаем метку для названия лабораторной работы
        self.label = QtWidgets.QLabel(f"Лабораторная работа {num_lab}")
        self.label.setStyleSheet("""
            font-size: 24px;
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label,
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        # Создаем выпадающий список (combobox) для выбора задания
        self._create_combobox()

        # Создаем блок с условием задачи
        self._create_question()

        # Создаем блоки для ввода и вывода данных
        self._create_input_output_data()

        # Создаем кнопки "Ок" и "Отмена"
        self._create_button()

    def _create_input_output_data(self):
        """
        Создает блоки для ввода и вывода данных.
        """
        # Создаем поле для ввода данных (однострочное)
        self.input_data = QtWidgets.QLineEdit("1 2 3 4")
        self.input_data.setPlaceholderText("Input data: ")

        # Создаем блок для вывода данных (многострочное)
        self.output_data = QtWidgets.QTextEdit()
        self.output_data.setPlaceholderText("Output data: ")
        self.output_data.setReadOnly(True)

        # Создаем разделитель (splitter) для блоков ввода и вывода с настройкой размеров
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        splitter.addWidget(self.input_data)
        splitter.addWidget(self.output_data)
        splitter.setSizes([200, 100])
        self.layout.addWidget(splitter, 3)

    def _create_question(self):
        """
        Создание места для условия, динамически должен обновляться в зависимости от выбора в combobox и TabWidget
        """
        self.label = QtWidgets.QLabel(
            "Напишите программу для решения примера. Есть переменные: a,b,c,k: Предусмотрите деление на 0. "
            "\nВсе необходимые переменные вводите ниже.")
        # Позволяет переносить текст на следующую строку, если не помещается
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label, 2,
                              alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

    def _create_combobox(self):
        """
        Создает выпадающий список (combobox) для выбора задания.
        """
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems([
            "Задание 1", "Задание 2",
            "Задание 3", "Задание 4"
        ])
        self.layout.addWidget(self.combobox, 0,
                              alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)

    def _create_button(self):
        """
        Создает кнопки "Ок" и "Отмена" и добавляет их в QDialogButtonBox.
        """
        buttons = QtWidgets.QDialogButtonBox()
        buttons.setStyleSheet(buttons.styleSheet() +
                              """
                              border-style: outset;
                              border-width: 1px;
                              border-radius: 15px;
                              border-color: rgb(20, 20, 20);
                              padding: 4px;
                              """
                              )
        self.ok_button = buttons.addButton(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.cancel_button = buttons.addButton(QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        self.layout.addWidget(buttons)
