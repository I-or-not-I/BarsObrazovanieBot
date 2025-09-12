import abc
from aiogram import Router
from aiogram.types import BotCommand

from src.template_engine import AbstractTemplateEngine


class AbstractHandler(abc.ABC):
    @abc.abstractmethod
    def __init__(self, template_engine: AbstractTemplateEngine) -> None:
        pass

    @abc.abstractmethod
    async def get_router(self) -> Router:
        pass

    @abc.abstractmethod
    async def get_commands(self) -> list[BotCommand]:
        pass
