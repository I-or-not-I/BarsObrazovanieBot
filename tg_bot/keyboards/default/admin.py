from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.abstract_keyboard import AbstractReplyKeyboard


class AdminAllMarkupsKeyboard(AbstractReplyKeyboard):
    def __init__(self) -> None:
        self.__all_admins = "Все админы"
        self.__add_admin = "Добавить админа"
        self.__del_admin = "Удалить админа"

    def get_keyboard(self) -> ReplyKeyboardMarkup:
        buttons: list = [
            [KeyboardButton(text=self.__all_admins)],
            [KeyboardButton(text=self.__add_admin)],
            [KeyboardButton(text=self.__del_admin)],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
