from aiogram.fsm.state import StatesGroup, State


class StartStates(StatesGroup):
    START = State()
    ANSWER_FOR_PASSWORD = State()
    DONE = State()
