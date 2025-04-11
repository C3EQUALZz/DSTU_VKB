from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class AIBotResponseStateMachine(StatesGroup):
    wait = State()
