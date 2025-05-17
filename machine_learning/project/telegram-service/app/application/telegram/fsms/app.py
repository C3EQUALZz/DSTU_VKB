from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class ImageStateGroup(StatesGroup):
    WAITING_PHOTO = State()
    ACTION_SELECTION = State()
    ROTATE_ANGLE = State()
    CROP_PARAMS = State()


class TextStateGroup(StatesGroup):
    ACTIVATE = State()
    WAITING = State()
    PROCESSING = State()


class StartStateGroup(StatesGroup):
    WAITING = State()


class AppState(StatesGroup):
    # Общие состояния
    IDLE = State()

    IMAGE = ImageStateGroup()
    TEXT = TextStateGroup()

    PROCESSING = State()
