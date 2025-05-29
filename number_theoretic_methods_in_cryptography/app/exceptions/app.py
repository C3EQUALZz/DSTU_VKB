import traceback

from CTkMessagebox import CTkMessagebox


def show_error_dialog(message: str, details: str = None) -> None:
    """
    Показывает диалоговое окно с ошибкой
    """

    msg = CTkMessagebox(
        title="Критическая ошибка",
        message=message,
        icon="cancel",
        option_1="Показать детали",
        option_2="Закрыть"
    )

    if msg.get() == "Показать детали" and details:
        detail_box = CTkMessagebox(
            title="Детали ошибки",
            message=details,
            icon="cancel",
            option_1="Закрыть"
        )
        detail_box.get()


def global_exception_handler(exc_type, exc_value, exc_traceback):
    """
    Глобальный обработчик исключений
    """
    if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
        return

    # Формируем сообщение
    error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    error_message = f"Произошла непредвиденная ошибка:\n\n{exc_value}"

    # print("Необработанное исключение:")
    # print(error_details)

    # Показываем ошибку через Tk
    show_error_dialog(error_message, error_details)
