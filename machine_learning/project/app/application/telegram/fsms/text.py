from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class TextStateMachine(StatesGroup):
    """
    FSM which describes state of bot.
    It was made for flooding block and changing states of bot.
    """
    wait_for_message: State = State()
    processing: State = State()
