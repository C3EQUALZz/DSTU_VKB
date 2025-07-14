from aiogram.fsm.state import StatesGroup, State


class SimpleDataPermutationStartStates(StatesGroup):
    START = State()
    CHOOSE_ENCRYPT_OR_DECRYPT = State()
