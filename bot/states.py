from aiogram.fsm.state import State, StatesGroup


class LocationState(StatesGroup):
    waiting_for_location = State()
