from aiogram.fsm.state import State, StatesGroup


class SupportState(StatesGroup):
    waiting_message = State()
