from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    admin_id = State()
