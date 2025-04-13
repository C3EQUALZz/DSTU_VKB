from aiogram.fsm.state import StatesGroup, State


class ImageStateGroup(StatesGroup):
    ACTIVATE = State()
    WAITING = State()
    PROCESSING = State()


class TextStateGroup(StatesGroup):
    ACTIVATE = State()
    WAITING = State()
    PROCESSING = State()


class AppState(StatesGroup):
    # Общие состояния
    IDLE = State()

    IMAGE = ImageStateGroup()
    TEXT = TextStateGroup()

    PROCESSING = State()
