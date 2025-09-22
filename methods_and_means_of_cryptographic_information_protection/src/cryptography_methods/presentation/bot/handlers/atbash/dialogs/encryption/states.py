from aiogram.fsm.state import StatesGroup, State


class EncryptAtbashDialogStates(StatesGroup):
    ASK_TEXT = State()
