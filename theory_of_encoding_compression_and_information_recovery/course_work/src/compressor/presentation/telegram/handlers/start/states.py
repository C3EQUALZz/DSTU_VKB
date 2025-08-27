from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    START = State()
    LINK_TELEGRAM = State()
    DONE = State()
