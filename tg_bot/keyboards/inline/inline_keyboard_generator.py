from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.abstract_keyboard import AbstractInlineKeyboard


class InlineKeyboardGenerator(AbstractInlineKeyboard):
    async def get_keyboard(self, options: dict, callback_data_prefix: str) -> InlineKeyboardMarkup:
        buttons: list = [
            [InlineKeyboardButton(text=option, callback_data=f"{callback_data_prefix}_{options[option]}")]
            for option in options.keys()
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
