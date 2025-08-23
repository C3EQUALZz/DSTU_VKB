from aiogram.fsm.state import StatesGroup, State


class CompressStates(StatesGroup):
    START = State()
    ANSWER_WHAT_TO_COMPRESS = State()


class CompressBinaryOrTextFileStates(StatesGroup):
    START = State()
    ASK_FILE = State()
    DONE = State()
