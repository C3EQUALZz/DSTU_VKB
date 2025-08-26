from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    START = State()
    ANSWER_FOR_PASSWORD = State()
    DONE = State()
