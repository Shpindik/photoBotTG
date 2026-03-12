from aiogram.fsm.state import State, StatesGroup


class LocationState(StatesGroup):
    waiting_for_location = State()


class PhoneState(StatesGroup):
    waiting_for_phone = State()


class ProblemState(StatesGroup):
    waiting_for_description = State()
