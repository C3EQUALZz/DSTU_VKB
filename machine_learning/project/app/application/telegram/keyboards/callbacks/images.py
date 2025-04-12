from aiogram.filters.callback_data import CallbackData


class ImageClickActionCallback(CallbackData, prefix="action"):
    name: str
