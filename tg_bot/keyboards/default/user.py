from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.abstract_keyboard import AbstractReplyKeyboard


class UserAllMarkupsKeyboard(AbstractReplyKeyboard):
    def __init__(self) -> None:
        self.__person_data = "Личные данные"
        self.__summary_marks = "Сводка оценок"
        self.__week_schedule = "Расписание на неделю"
        self.__school_info = "Информация о школе"

    def get_keyboard(self) -> ReplyKeyboardMarkup:
        buttons: list = [
            [KeyboardButton(text=self.__person_data), KeyboardButton(text=self.__summary_marks)],
            [KeyboardButton(text=self.__week_schedule), KeyboardButton(text=self.__school_info)],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


class UserNotLoggedMarkupsKeyboard(AbstractReplyKeyboard):
    def __init__(self) -> None:
        self.__login = "Войти"

    def get_keyboard(self) -> ReplyKeyboardMarkup:
        buttons: list = [
            [KeyboardButton(text=self.__login)],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
