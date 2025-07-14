from aiogram.fsm.state import StatesGroup, State


class SimpleDataPermutationEncryptionStates(StatesGroup):
    TABLE_WIDTH = State()
    TABLE_HEIGHT = State()
    DATA = State()
