from aiogram.fsm.state import StatesGroup, State


class SimpleDataPermutationDecryptionStates(StatesGroup):
    TABLE_WIDTH = State()
    TABLE_HEIGHT = State()
    DATA = State()
