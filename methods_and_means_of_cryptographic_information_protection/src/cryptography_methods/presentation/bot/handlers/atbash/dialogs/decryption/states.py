from aiogram.fsm.state import StatesGroup, State


class DecryptAtbashDialogStates(StatesGroup):
    ASK_TEXT = State()
