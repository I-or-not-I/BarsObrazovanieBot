import abc
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


class AbstractReplyKeyboard(abc.ABC):
    @abc.abstractmethod
    async def get_keyboard(self, *args, **kwargs) -> ReplyKeyboardMarkup:
        pass


class AbstractInlineKeyboard(abc.ABC):
    @abc.abstractmethod
    async def get_keyboard(self, *args, **kwargs) -> InlineKeyboardMarkup:
        pass
