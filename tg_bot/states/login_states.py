from aiogram.fsm.state import StatesGroup, State


class LoginStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()
    waiting_for_sms_code = State()
