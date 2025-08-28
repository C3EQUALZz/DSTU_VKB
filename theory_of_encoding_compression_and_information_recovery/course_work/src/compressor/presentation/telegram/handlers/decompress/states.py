from aiogram.fsm.state import State, StatesGroup


class DecompressStates(StatesGroup):
    START = State()
    ANSWER_WHAT_TO_COMPRESS = State()


class DecompressBinaryOrTextFileStates(StatesGroup):
    START = State()
    ASK_FILE = State()
    DONE = State()
