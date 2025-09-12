from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.abstract_keyboard import AbstractReplyKeyboard


class AllMarkupsKeyboard(AbstractReplyKeyboard):
    def __init__(self) -> None:
        self.__start = "/start"

    def get_keyboard(self) -> ReplyKeyboardMarkup:
        buttons: list = [
            [KeyboardButton(text=self.__start)],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
