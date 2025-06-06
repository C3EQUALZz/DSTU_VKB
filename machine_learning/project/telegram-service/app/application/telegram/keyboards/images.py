from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext
from aiogram_i18n.types import InlineKeyboardButton

from app.application.telegram.keyboards.callbacks.images import (
    ImageCLickAction,
    ImageClickActionCallback,
)


def build_keyboard(i18n: I18nContext) -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for action in ImageCLickAction:
        builder.row(
            InlineKeyboardButton(
                text=i18n.get(action), callback_data=ImageClickActionCallback(action=action).pack()
            )
        )

    return builder
