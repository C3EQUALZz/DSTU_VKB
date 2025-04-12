from typing import Final

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback


def build_keyboard(i18n: I18nContext) -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # По 1 или 2 кнопки в строке

    button_labels: Final[list[str]] = [
        i18n.get("gray-to-color"),
    ]

    for label in button_labels[:-2]:
        builder.row(
            InlineKeyboardButton(
                text=label,
                callback_data=ImageClickActionCallback(name=label).pack()
            )
        )

    # Последнюю строку делаем с двумя кнопками
    builder.row(
        InlineKeyboardButton(
            text=button_labels[-2],
            callback_data=ImageClickActionCallback(name=button_labels[-2]).pack()
        ),
        InlineKeyboardButton(
            text=button_labels[-1],
            callback_data=ImageClickActionCallback(name=button_labels[-1]).pack()
        )
    )

    return builder
